from flask import Flask, render_template, request
from werkzeug.datastructures.file_storage import FileStorage

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

    # -----------------------------
    # Upload Multiple Resumes
    # -----------------------------
    resume_files = request.files.getlist("resume")

    resume_paths = []

    for resume_file in resume_files:
        resume_path = "resumes/" + resume_file.filename
        resume_file.save(resume_path)
        resume_paths.append(resume_path)

    print("STEP 2")

    # -----------------------------
    # Upload Job Description
    # -----------------------------
    job_file: FileStorage = request.files["job"]

    job_path = "jobs/" + job_file.filename

    job_file.save(job_path)

    print("STEP 3")

    # -----------------------------
    # Read Resume
    # -----------------------------
    results = []

    for resume_path in resume_paths:

        resume_text = read_resume(resume_path)

        print("\n========== RESUME TEXT ==========\n")
        print(resume_text)
        print("\n===============================\n")

        # Calculate ATS, generate summary, etc.

        print("STEP 4")

        # -----------------------------
        # AI Interview Questions
        # -----------------------------
        ai_questions = generate_interview_questions(resume_text)

        print("STEP 5")

        # -----------------------------
        # Read Job Description
        # -----------------------------
        job_text = read_job(job_path)
        print("\n=========== JOB DESCRIPTION ===========")
        print(job_text)
        print("Length =", len(job_text))
        print("=======================================")

        # -----------------------------
        # AI Project Recommendations
        # -----------------------------
        projects = generate_projects(resume_text)
        roadmap = generate_roadmap(resume_text)


        print("STEP 5.5")
        print(projects)
        print(roadmap)

        print("STEP 6")

        # -----------------------------
        # Extract Skills
        # -----------------------------
        skills = []

        for line in job_text.splitlines():

            line = line.strip()

            if line != "":
                skills.append(line)

        print("STEP 7")

        # -----------------------------
        # Match Skills
        # -----------------------------
        matched = match_skills(
            resume_text,
            skills
        )

        print("STEP 8")

        # -----------------------------
        # Missing Skills
        # -----------------------------
        missing = []

        for skill in skills:

            if skill not in matched:

                missing.append(skill)

        print("STEP 9")

        # -----------------------------
        # ATS Score
        # -----------------------------
        score = calculate_ats(
            matched,
            len(skills)
        )

        print("STEP 10")

        # -----------------------------
        # AI Candidate Insights
        # -----------------------------
        insights = generate_candidate_insights(
            score,
            matched,
            missing
        )

        # -----------------------------
        # Recommendation
        # -----------------------------

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

        print("STEP 11")

        # -----------------------------
        # Candidate Summary
        # -----------------------------
        # 
        # 
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

        print("STEP 12")

        # -----------------------------
        # Show Result
        # -----------------------------
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

    # ----------------------------------
    # Upload Job Description
    # ----------------------------------
    job_file = request.files["job"]

    job_path = "jobs/" + job_file.filename

    job_file.save(job_path)

    # Read Job Description
    job_text = read_job(job_path)

    # ----------------------------------
    # Extract Required Skills
    # ----------------------------------
    skills = []

    for line in job_text.splitlines():

        line = line.strip()

        if line != "":
            skills.append(line)

    # ----------------------------------
    # Upload Multiple Resumes
    # ----------------------------------
    resume_files = request.files.getlist("resume")

    results = []

    # ----------------------------------
    # Analyze Every Resume
    # ----------------------------------
    for resume in resume_files:

        # Save Resume
        resume_path = "resumes/" + resume.filename
        resume.save(resume_path)

        # Read Resume
        resume_text = read_resume(resume_path)

        # Match Skills
        matched = match_skills(resume_text, skills)

        # Missing Skills
        missing = []

        for skill in skills:
            if skill not in matched:
                missing.append(skill)

        # ATS Score
        score = calculate_ats(
            matched,
            len(skills)
        )

        # Candidate Summary
        summary = f"""
Candidate matches {len(matched)} out of {len(skills)} required skills.

Overall ATS Score: {score:.1f}%

The profile demonstrates good technical alignment with the job requirements.
"""

        strengths = matched
        weaknesses = missing
        confidence = score

        why_ranked = []

        if score >= 80:
            why_ranked.append("Excellent overall ATS score")

        if len(matched) >= 5:
            why_ranked.append("Strong skill match with job description")

        if len(missing) <= 2:
            why_ranked.append("Very few missing skills")

        if len(matched) > len(missing):
            why_ranked.append("Technical profile closely aligns with the role")

        if len(why_ranked) == 0:
            why_ranked.append("Requires additional technical skill development")

        # Recommendation
        if score >= 80:
            recommendation = "⭐⭐⭐⭐⭐ Strong Hire"

        elif score >= 60:
            recommendation = "⭐⭐⭐⭐ Hire"

        else:
            recommendation = "⭐⭐ Consider"

        # Store Candidate Data
        results.append({

    "name": resume.filename,

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
    # ----------------------------------
    # Rank Candidates
    # ----------------------------------
    results.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    # ----------------------------------
    # Show HR Dashboard
    # ----------------------------------
    return render_template(

        "hr_result.html",

        results=results

    )

if __name__ == "__main__":
    app.run(debug=True)