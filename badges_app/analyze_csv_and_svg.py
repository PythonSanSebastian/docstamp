import argparse
from difflib import SequenceMatcher
import base64
import io
from fastapi import UploadFile
import xml.etree.ElementTree as ET
import re
from typing import List
from pdf2image import convert_from_bytes
import os
import shutil
import csv

from generate_badges import create_badges

# Known naming variants for each target field
KNOWN_VARIANTS = {
    'First Name': ['firstname', 'fname', 'givenname'],
    'Last Name': ['lastname', 'surname', 'lname', 'familyname'],
    'Company Name': ['companyname', 'company name', 'company', 'organization', 'employer'],
}


def normalize(name: str) -> str:
    """Normalize column name: remove special characters and lowercase it."""
    return re.sub(r'[\s_\-\.]', '', name).lower()


def best_match(variants, normalized_columns, used_columns):
    """Return the best match from normalized_columns for the given variants."""
    best_score = 0
    best_match_column = None

    for variant in variants:
        for column in normalized_columns:
            if column in used_columns:
                continue
            score = SequenceMatcher(None, variant, column).ratio()
            if score > best_score:
                best_score = score
                best_match_column = column

    return best_match_column if best_score >= 0.6 else None


def find_matching_columns(target, normalized_columns, used_columns, results):
    """Find best matching columns from a CSV file or a list of columns for the given target fields."""
    variants = KNOWN_VARIANTS.get(target, [target])
    match_column = best_match(variants, normalized_columns, used_columns)

    if match_column:
        matched_column = normalized_columns[match_column]
        used_columns.add(match_column)

        results[target] = {
            'csv_column': matched_column,
            'samples': []
        }
        return matched_column
    return ""


def find_matching_columns_from_list(columns: list, target_fields: list) -> dict:
    """Find best matching columns from a columns list for the given target fields."""
    normalized_columns = {normalize(c): c for c in columns}
    results = {}
    used_columns = set()

    for target in target_fields:
        matched_column = find_matching_columns(target, normalized_columns, used_columns, results)
        if not matched_column:
            results[target] = None

    return results


def find_matching_columns_from_csv(csv_file: str, target_fields: list) -> dict:
    """Find best matching columns from a CSV file for the given target fields."""
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        columns = next(reader)

        normalized_columns = {normalize(c): c for c in columns}
        results = {}
        used_columns = set()

        for target in target_fields:
            matched_column = find_matching_columns(target, normalized_columns, used_columns, results)
            if matched_column:
                # Collect up to 3 non-empty sample values
                file.seek(0)
                next(reader)  # Skip header again
                sample_count = 0
                for row in reader:
                    idx = columns.index(matched_column)
                    if idx >= len(row):
                        continue
                    value = row[idx].strip()
                    if value:
                        results[target]['samples'].append(value)
                        sample_count += 1
                    if sample_count >= 3:
                        break
            else:
                results[target] = None  # No match found

        return results


def print_analysis(results: dict):
    """Print the matching results in a readable format."""
    print("\nCSV Column Matching Results")
    print("=" * 50)

    for target, data in results.items():
        print(f"\nTarget field: '{target}'")
        if data:
            print(f"  Matched column: '{data['csv_column']}'")
            if data['samples']:
                print(f"  Sample values: {', '.join(data['samples'])}")
            else:
                print("  (No sample values found)")
        else:
            print("  No matching column found.")

    print("\n" + "=" * 50)


def list_of_strings(arg):
    return arg.split(',')


def svg_to_image(tmp_preview_dir, role, template_filename: str, template_vars) -> str:
    create_badges(template_filename, os.path.join(tmp_preview_dir, "preview_data.csv"), tmp_preview_dir, template_vars)

    with open(os.path.join(tmp_preview_dir, f"{role}_0.pdf"), "rb") as f:
        images = convert_from_bytes(f.read(), first_page=1, last_page=1)

    buffered = io.BytesIO()
    images[0].save(buffered, format="JPEG", quality=85)
    return base64.b64encode(buffered.getvalue()).decode()


def prepare_preview_data(tmp_preview_dir, template_vars):
    preview_data = {
        "First Name": "Klaus",
        "Last Name": "Templatemann",
        "Company Name": "Badgeify"
    }
    matches = find_matching_columns_from_list(template_vars, preview_data.keys())

    column_value_map = {}
    for target_key, data in matches.items():
        if data:
            column_name = data["csv_column"]
            column_value_map[column_name] = preview_data.get(target_key, "")

    row = [column_value_map.get(col, "") for col in template_vars]

    with open(os.path.join(tmp_preview_dir, "preview_data.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(template_vars or [","])
        writer.writerow(row or [","])


def analyze_svg_templates(svg_files: List[UploadFile], templates_dir: str):
    tmp_preview_dir = "tmp_preview"
    os.makedirs(tmp_preview_dir, exist_ok=True)
    pattern = re.compile(r"\{\{([^}]+)\}\}")
    results = {}
    previews = {}

    try:
        for svg_file in svg_files:
            template_filename = os.path.join(templates_dir, svg_file.filename)
            with open(os.path.join(templates_dir, svg_file.filename), "rb") as f:
                try:
                    root = ET.fromstring(f.read())
                    template_vars = set()
                    for elem in root.iter():
                        if elem.text and pattern.search(elem.text):
                            template_vars.update(pattern.findall(elem.text))
                        for attr in elem.attrib.values():
                            if pattern.search(attr):
                                template_vars.update(pattern.findall(attr))

                    results[svg_file.filename] = sorted(template_vars)
                    prepare_preview_data(tmp_preview_dir, template_vars)
                    previews[svg_file.filename] = svg_to_image(tmp_preview_dir, svg_file.filename.split('.')[0], template_filename, template_vars)
                except ET.ParseError as e:
                    print(f"Error parsing SVG {svg_file.filename}: {e}")
                    results[svg_file.filename] = ["Invalid SVG file"]
                    previews[svg_file.filename] = None

        return results, previews
    finally:
        shutil.rmtree(tmp_preview_dir, ignore_errors=True)


if __name__ == "__main__":
    TARGET_FIELDS = ['First Name', 'Last Name', 'Company Name']

    parser = argparse.ArgumentParser(
        description="Find matching columns in a CSV file."
    )
    parser.add_argument(
        "--csv_file",
        help="Path to the CSV file to analyze",
        type=str,
        default=None
    )
    parser.add_argument(
        "--columns",
        help="List of columns to analyze",
        type=list_of_strings,
        default=None
    )
    args = parser.parse_args()

    matches = {}
    if args.csv_file:
        matches = find_matching_columns_from_csv(args.csv_file, TARGET_FIELDS)
    elif args.columns:
        matches = find_matching_columns_from_list(args.columns, TARGET_FIELDS)
    print_analysis(matches)
