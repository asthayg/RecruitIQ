
import os

from flask import Flask, render_template, request
from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.utils import secure_filename

from utils.candidate_insights import generate_candidate_insights
from utils.resume_reader import read_resume
from utils.job_reader import read_job
from utils.skill_matcher import match_skills
from utils.ats_calculator import calculate_ats
from utils.ai_generator import generate_interview_questions
from utils.project_generator import generate_projects
from utils.roadmap_generator import generate_roadmap
from utils.hr_reviewer import generate_hr_review


app = Flask(__name__)

# Create upload directories automatically
os.makedirs("resumes", exist_ok=True)
os.makedirs("jobs", exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/student")
def student():
    return render_template("student_dashboard.html")


@app.route("/hr")
def hr():
    return render_template("hr_dashboard.html")


@app.route("/analyze_student", methods=["POST"])
def analyze_student():

    # Upload multiple resumes
    resume_files = request.files.getlist("resume")
    resume_paths = []

    for resume_file in resume_files:

        if not resume_file.filename:
            continue

        filename = secure_filename(resume_file.filename)
        resume_path = os.path.join("resumes", filename)

        resume_file.save(resume_path)
        resume_paths.append(resume_path)

    # Check whether resumes were uploaded
    if not resume_paths:
        return "Please upload at least one resume.", 400

    # Upload job description
    job_file: FileStorage = request.files["job"]

    if not job_file or not job_file.filename:
        return "Please upload a job description.", 400

    job_filename = secure_filename(job_file.filename)
    job_path = os.path.join("jobs", job_filename)

    job_file.save(job_path)

    # Read job description
    job_text = read_job(job_path)

    # Extract required skills
    skills = []

    for line in job_text.splitlines():

        line = line.strip()

        if line != "":
            skills.append(line)

    # Process uploaded resumes
    results = []

    for resume_path in resume_paths:

        # Read resume
        resume_text = read_resume(resume_path)

        print("\n========== RESUME TEXT ==========\n")
        print(resume_text)
        print("\n===============================\n")

        # Generate AI interview questions
        ai_questions = generate_interview_questions(resume_text)

        # Generate AI project recommendations
        projects = generate_projects(resume_text)

        # Generate personalized career roadmap
        roadmap = generate_roadmap(resume_text)

        # Match skills
        matched = match_skills(
            resume_text,
            skills
        )

        # Identify missing skills
        missing = []

        for skill in skills:

            if skill not in matched:
                missing.append(skill)

        # Calculate ATS score
        score = calculate_ats(
            matched,
            len(skills)
        )

        # Generate candidate insights
        insights = generate_candidate_insights(
            score,
            matched,
            missing
        )

        # Generate recommendation
        if score >= 80:

            recommendation = """
Excellent Profile ⭐⭐⭐⭐⭐

The candidate is highly suitable for this role.

Proceed with the technical interview.
"""

        elif score >= 60:

            recommendation = """
Good Profile ⭐⭐⭐⭐

The candidate has good potential.

Improve the missing skills to increase hiring chances.
"""

        else:

            recommendation = """
Needs Improvement ⭐⭐

The candidate should improve technical skills before applying.
"""

        # Candidate summary
        summary = f"""
<b style='color:#7C3AED;font-size:18px;'>Candidate Overview</b><br><br>

<b>Current ATS Score:</b> {score}%<br><br>

<b>Matched Skills:</b><br>
{', '.join(matched)}<br><br>

<b>Skills to Improve:</b><br>
{', '.join(missing)}<br><br>

<b>Recommended Roles:</b><br>

• AI/ML Intern<br>
• Data Analyst<br>
• Python Developer<br>
• Machine Learning Engineer<br><br>

<b>Overall Assessment:</b><br>

The candidate demonstrates a solid foundation in AI, Machine Learning, Python and Data Analysis. Strengthening the missing skills will improve hiring potential.
"""

        print("Student analysis completed.")

        # Display student result
        return render_template(
            "result.html",
            score=score,
            matched=matched,
            missing=missing,
            recommendation=recommendation,
            summary=summary,
            ai_questions=ai_questions,
            projects=projects,
            roadmap=roadmap,
            insights=insights
        )


@app.route("/analyze_hr", methods=["POST"])
def analyze_hr():

    # Upload job description
    job_file = request.files["job"]

    if not job_file or not job_file.filename:
        return "Please upload a job description.", 400

    job_filename = secure_filename(job_file.filename)
    job_path = os.path.join("jobs", job_filename)

    job_file.save(job_path)

    # Read job description
    job_text = read_job(job_path)

    # Extract required skills
    skills = []

    for line in job_text.splitlines():

        line = line.strip()

        if line != "":
            skills.append(line)

    # Upload multiple resumes
    resume_files = request.files.getlist("resume")

    results = []

    # Analyze every resume
    for resume in resume_files:

        if not resume.filename:
            continue

        # Save resume
        filename = secure_filename(resume.filename)
        resume_path = os.path.join("resumes", filename)

        resume.save(resume_path)

        # Read resume
        resume_text = read_resume(resume_path)

        # Match skills
        matched = match_skills(
            resume_text,
            skills
        )

        # Identify missing skills
        missing = []

        for skill in skills:

            if skill not in matched:
                missing.append(skill)

        # Calculate ATS score
        score = calculate_ats(
            matched,
            len(skills)
        )

        # Candidate summary
        summary = f"""
Candidate matches {len(matched)} out of {len(skills)} required skills.

Overall ATS Score: {score:.1f}%

The profile demonstrates good technical alignment with the job requirements.
"""

        strengths = matched
        weaknesses = missing
        confidence = score

        # Explain candidate ranking
        why_ranked = []

        if score >= 80:
            why_ranked.append("Excellent overall ATS score")

        if len(matched) >= 5:
            why_ranked.append("Strong skill match with job description")

        if len(missing) <= 2:
            why_ranked.append("Very few missing skills")

        if len(matched) > len(missing):
            why_ranked.append(
                "Technical profile closely aligns with the role"
            )

        if len(why_ranked) == 0:
            why_ranked.append(
                "Requires additional technical skill development"
            )

        # Hiring recommendation
        if score >= 80:

            recommendation = "⭐⭐⭐⭐⭐ Strong Hire"

        elif score >= 60:

            recommendation = "⭐⭐⭐⭐ Hire"

        else:

            recommendation = "⭐⭐ Consider"

        # Store candidate data
        results.append({

            "name": filename,
            "score": score,
            "matched": matched,
            "missing": missing,
            "recommendation": recommendation,
            "summary": summary,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "confidence": confidence,
            "why_ranked": why_ranked

        })

    # Rank candidates by ATS score
    results.sort(
        key=lambda x: x.get("score", 0),
        reverse=True
    )

    # Display HR dashboard
    return render_template(
        "hr_result.html",
        results=results
    )


if __name__ == "__main__":
    app.run(debug=True)
