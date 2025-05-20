import io
import os
import shutil
import zipfile
from typing import List

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from generate_badges import create_all_badges, MissingCSVFieldsException
from merge_badges_into_pdf import BadgeMerger
from analyze_csv_and_svg import analyze_svg_templates


app = FastAPI(title="Badge Generator")
app.mount("/static", StaticFiles(directory="static"), name="static")
TEMPLATES = Jinja2Templates(directory="templates")
ERROR_MESSAGE = (
    "We’re unable to proceed with badge generation.<br><br>"
    "<strong>Suggested steps:</strong><br>"
    "&bull; Verify your input files for accuracy<br>"
    "&bull; Ensure all required data is provided<br>"
    "&bull; Try the process again"
)
UPLOAD_TEMPLATES_DIR = "uploaded_templates"
UPLOAD_DATA_DIR = "uploaded_data"
GENERATED_DIR = "generated_badges"


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "app_name": "Conference Badge Manager"}
    )


@app.post("/analyze-svg")
async def analyze_svg(
    request: Request,
    svg_files: List[UploadFile] = File(...)
):
    try:
        save_uploaded_files(svg_files, UPLOAD_TEMPLATES_DIR)
        results, previews = analyze_svg_templates(svg_files, UPLOAD_TEMPLATES_DIR)
        return TEMPLATES.TemplateResponse(
            "index.html",
            {"request": request, "results": results, "app_name": "SVG Analysis", "previews": previews}
        )
    except Exception as e:
        print("Error: %s" % str(e))
        return render_error_page(
            request,
            "Failed to analyze SVG files",
            "We’re unable to proceed with SVG Analysis"
        )


@app.post("/generate-badges")
async def generate_badges(
    request: Request,
    badge_width: float = Form(...),
    badge_height: float = Form(...),
    output_format: str = Form(...),
    data_files: List[UploadFile] = File(...),
    svg_analysis_results: str = Form(...),
):
    try:
        roles, error_response = validate_templates_and_data_files(request, data_files)
        if error_response:
            return error_response

        save_uploaded_files(data_files, UPLOAD_DATA_DIR)
        create_all_badges(roles, UPLOAD_TEMPLATES_DIR, UPLOAD_DATA_DIR, GENERATED_DIR, svg_analysis_results.replace("'", '"'))

        if output_format == "merged":
            return return_merged_badges(request, badge_width, badge_height)
        else:
            return return_separate_badges(request)
    except MissingCSVFieldsException as e:
        return render_error_page(
            request,
            "Badge Generation Failed",
            str(e)
        )
    except Exception as e:
        print("Error: %s" % str(e))
        return render_error_page(
            request,
            "Badge Generation Failed",
            ERROR_MESSAGE
        )
    finally:
        shutil.rmtree(UPLOAD_TEMPLATES_DIR, ignore_errors=True)
        shutil.rmtree(UPLOAD_DATA_DIR, ignore_errors=True)


@app.get("/download/{filename}")
async def download_file(filename: str):
    try:
        return FileResponse(
            filename,
            media_type="application/pdf",
            filename=filename
        )
    finally:
        shutil.rmtree(GENERATED_DIR, ignore_errors=True)


def render_error_page(request: Request, error_title: str, error_details: str):
    return TEMPLATES.TemplateResponse(
        "error.html",
        {
            "request": request,
            "app_name": "Conference Badge Manager",
            "error_title": error_title,
            "error_details": error_details
        }
    )


def save_uploaded_files(files, directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

    for template in files:
        path = os.path.join(directory, template.filename)
        with open(path, "wb") as buffer:
            shutil.copyfileobj(template.file, buffer)


def validate_templates_and_data_files(request, data_files):
    template_files = os.listdir(UPLOAD_TEMPLATES_DIR) if os.path.exists(UPLOAD_TEMPLATES_DIR) else []
    if not template_files or not data_files:
        return [], render_error_page(
            request,
            "Missing Files",
            "Both template and data files are required"
        )

    # Check for matching pairs
    template_names = {f.split('.')[0] for f in template_files}
    data_names = {f.filename.split('.')[0] for f in data_files}

    missing_templates = data_names - template_names
    missing_data = template_names - data_names

    if missing_templates:
        return [], render_error_page(
            request,
            "Missing Templates",
            f"Missing template files for these roles: {', '.join(missing_templates)}"
        )

    if missing_data:
        return [], render_error_page(
            request,
            "Missing Data Files",
            f"Missing data files for these roles: {', '.join(missing_data)}"
        )
    return data_names, None


def build_success_response(request: Request, filename: str):
    return TEMPLATES.TemplateResponse(
        "index.html",
        {
            "request": request,
            "download_url": f"/download/{filename}",
            "success": True,
            "app_name": "Conference Badge Manager"
        }
    )

def return_merged_badges(request, badge_width, badge_height):
    merger = BadgeMerger(badge_width_cm=badge_width, badge_height_cm=badge_height)
    output_pdf = "merged_badges.pdf"
    merger.merge_badges(GENERATED_DIR, output_pdf)
    return build_success_response(request, output_pdf)


def pack_badges_into_zip(output_dir):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        files = os.listdir(output_dir)
        for file_path in files:
            zip_file.write(os.path.join(output_dir, file_path), file_path)
    zip_buffer.seek(0)
    return zip_buffer


def return_separate_badges(request):
    zip_buffer = pack_badges_into_zip(GENERATED_DIR)
    zip_filename = "generated_badges.zip"
    with open(zip_filename, "wb") as f:
        f.write(zip_buffer.getvalue())
    return build_success_response(request, zip_filename)
