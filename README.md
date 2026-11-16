
# RecruitIQ
### AI-Powered Recruitment Intelligence Platform

RecruitIQ is a Flask-based recruitment support application that helps candidates and HR teams review resume-to-job-description alignment. It combines rule-based skill matching and ATS-style scoring with Groq-powered AI features for interview questions, project recommendations, and personalized career roadmaps.

<p align="center">
  <a href="https://recruitiq-zcwq.onrender.com/"><strong>🚀 Live Demo</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/asthayg/RecruitIQ"><strong>📂 Source Code</strong></a>
</p>

---

## Overview

RecruitIQ provides two workflows:

- **Student portal:** Review a resume against a supplied job description and receive an ATS-style score, matched and missing skills, AI-generated interview questions, project suggestions, and a career roadmap.
- **HR portal:** Upload a job description and multiple resumes, compare skill matches, calculate ATS-style scores, and view candidates ranked by score.

> **Important:** ATS-style scores are heuristic decision-support indicators, not validated measures of job performance. Human review is essential.

## Features

### Student Portal
- Resume and job-description upload
- PDF resume text extraction
- Skill matching
- ATS-style score calculation
- Missing skill detection
- AI-generated interview questions
- AI project recommendations
- Personalized career roadmap
- Candidate insights

### HR Portal
- Multiple resume uploads
- Job-description-based skill matching
- Candidate ranking
- ATS-style scoring
- Skill gap analysis
- Hiring recommendation labels
- Ranking explanations

## Technology Stack

| Area | Technologies |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| AI Integration | Groq API, Llama model |
| Resume Parsing | PyMuPDF |
| Application Server | Gunicorn |
| Configuration | python-dotenv |
| Deployment | Render |
| Version Control | Git, GitHub |

## How It Works

1. Upload a resume and job description.
2. Extract text from the uploaded documents.
3. Compare resume content with job requirements.
4. Calculate an ATS-style score.
5. Identify matched and missing skills.
6. Generate AI-powered career recommendations and interview questions.
7. Display candidate analysis and ranking results.

## Project Structure

```text
RecruitIQ/
├── app.py
├── requirements.txt
├── .env.example
├── utils/
│   ├── ai_generator.py
│   ├── ats_calculator.py
│   ├── candidate_insights.py
│   ├── hr_reviewer.py
│   ├── job_reader.py
│   ├── project_generator.py
│   ├── roadmap_generator.py
│   ├── resume_reader.py
│   └── skill_matcher.py
├── templates/
├── static/
├── resumes/
└── jobs/
```

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/asthayg/RecruitIQ.git
cd RecruitIQ/RecruitIQ
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows PowerShell**
```powershell
.\venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your Groq API key

Create a `.env` file beside `app.py`:

```env
GROQ_API_KEY=your_groq_api_key
```

Get your API key from the [Groq Console](https://console.groq.com/keys).

Never commit your `.env` file or expose API credentials.

### 5. Run the application

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Deployment

The live application is hosted on Render.

- Root directory: `RecruitIQ`
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Environment variable: `GROQ_API_KEY`

The free Render service may spin down after inactivity. Its local filesystem is ephemeral, so uploaded files are not persistent.

## Privacy and Responsible Use

- Use fictional resumes for public demonstrations.
- Do not upload personal candidate information without appropriate permission.
- Review AI-generated content for accuracy.
- Treat scores as decision-support indicators, not automatic hiring decisions.
- Store API credentials securely using environment variables.

## Current Limitations

- Resume extraction currently uses PyMuPDF; scanned PDFs may require OCR.
- ATS scoring is heuristic and depends on resume and job-description wording.
- Persistent candidate history and production user accounts are not currently implemented.
- Uploaded files are saved locally and are not persistent on Render's free service.

## Future Improvements

- [ ] Secure authentication and role-based access
- [ ] Database-backed analysis history
- [ ] Persistent file storage
- [ ] File type and upload-size validation
- [ ] Improved skill normalization and weighted matching
- [ ] Downloadable candidate reports
- [ ] Automated testing and structured logging
- [ ] Responsive and accessible UI improvements

## Developed By

**Astha Singh**

- GitHub: [@asthayg](https://github.com/asthayg)
- Live Demo: https://recruitiq-zcwq.onrender.com/

---

If you find this project useful, feel free to explore the repository and share feedback.
