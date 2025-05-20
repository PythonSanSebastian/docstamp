# Conference Badge Generator WebApp

A web application for generating conference badges from SVG templates and participant CSV data.

## Features

- Upload multiple SVG badge templates
- Upload multiple CSV files with attendee data
- Two output options:
  - Separate PDF files for each badge
  - Single merged PDF with 4 badges per page (with customizable dimensions)

## 🚀 Quick Start with Docker

1. Navigate to the project directory:

```bash
cd badges_app
```

2. Build the Docker image:

```bash
docker build -t badge-generator .
```

3. Run the container:

```bash
docker run -d -p 8000:8000 --name badge-app badge-generator
```

4. Open the app in your browser: http://localhost:8000
