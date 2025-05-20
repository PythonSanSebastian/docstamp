import csv
import json
import os
import shutil
import subprocess


class MissingCSVFieldsException(Exception):
    def __init__(self, svg_filename, csv_filename, missing_fields):
        message = f"""
        We’re unable to proceed with badge generation.<br><br>
        <strong>Details:</strong><br>
        The following fields are used in the badge template <code>{os.path.basename(svg_filename)}</code> but they are missing in the uploaded CSV file <code>{os.path.basename(csv_filename)}</code>:<br>
        <ul>
          {missing_fields}
        </ul>
        <br>
        <strong>Please check your CSV file and ensure all required fields are present</strong>
        """
        super().__init__(message)


def check_svg_and_csv_consistency(svg_file, csv_file, svg_analysis):
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        columns = next(reader)

        missing_fields = [field for field in svg_analysis if field not in columns]
        if missing_fields:
            raise MissingCSVFieldsException(svg_file, csv_file, missing_fields)


def create_badges(template_file, input_file, output_dir, svg_analysis):
    check_svg_and_csv_consistency(template_file, input_file, svg_analysis)

    cmd = f'docstamp create -i {input_file} -t {template_file} -d pdf -o {output_dir} --index ""'
    print('Calling {}'.format(cmd))
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    _stdout, stderr = process.communicate()
    if stderr and b'Failed to get connection' not in stderr:
        raise Exception(stderr.decode())


def create_all_badges(roles, templates_dir, data_dir, output_dir, svg_analysis_results):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    for role in roles:
        create_badges(
            os.path.join(templates_dir, f"{role}.svg"), os.path.join(data_dir, f"{role}.csv"), output_dir,
            json.loads(svg_analysis_results)[f"{role}.svg"]
        )
