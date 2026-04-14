# Survey Analytics Dashboard

A full-stack data visualization platform built to transform raw Excel survey data into actionable insights. This project features a React-based frontend and a Django REST Framework backend, deployed on AWS EC2 using Nginx.

The system processes structured Excel survey files, where the actual column headers were located in the second row of the dataset rather than the first row. I specifically configured the import logic to reference the second column in order to correctly map and interpret the expected field names based on the file’s unique structure. This ensured accurate data parsing and prevented schema mismatches during ingestion.

The platform dynamically aggregates the processed data into interactive charts and dashboards, enabling real-time demographic and behavioral analysis.

## Live Demo

URL: [DEMO](http://13.218.123.136/)  

## 🛠 Tech Stack

- Frontend: React.js, Tailwind CSS, Chart.js/Recharts, Axios
- Backend: Django, Django REST Framework, Pandas (Data Processing)
- Database: SQLite (Development/MVP)
- Deployment: AWS EC2 (Ubuntu), Nginx, Gunicorn/Nohup

## Key Features

- Excel Import: Seamlessly upload .xlsx survey results.
- Dynamic Analytics: Automated calculation of demographics and response trends.
- Live Status Monitoring: Real-time backend connectivity check.
- Responsive Design: Optimized for both desktop and mobile viewing.

## Project Structure

```text
├── survey_backend/          # Django Project
│   ├── analytics/           # API Logic & Excel Processing
│   ├── core/                # Settings & Routing
│   └── manage.py
├── survey_frontend/         # React Project
│   ├── src/                 # Components & App Logic
│   └── build/               # Production Build Files
└── nginx/                   # Configuration files
