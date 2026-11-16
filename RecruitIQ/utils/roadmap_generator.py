import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_roadmap(resume_text):

    prompt = f"""
You are RecruitIQ's Senior AI Career Mentor with over 15 years of experience in AI, Machine Learning, Data Science, Software Engineering, and Career Coaching.

Below is the candidate's resume.

=========================
{resume_text}
=========================

Analyze ONLY the resume above.

Generate a premium personalized career roadmap.

The report must sound like it was written by an experienced industry mentor.

Do NOT generate generic advice.

Return ONLY the following sections.

Current Level:

Write a professional paragraph (100-150 words) describing:

• Current technical strengths
• Practical experience
• Problem-solving ability
• Industry readiness
• Areas requiring improvement

Career Goal:

Write a professional paragraph (80-120 words) describing:

• Suitable AI career path
• Long-term growth
• Required technologies
• Industry expectations

Phase 1 (0-1 Month)

Create ONLY these subsections.

Technical Skills

Write exactly 5 detailed points.

Each point should contain 20–30 words.

Each point must explain WHY the task is important.

Do not write single-word bullets.

Each point should begin with ✔

Projects

Recommend exactly 2 real-world projects.

Explain each project in one sentence.

Practice Goals

Write exactly 5 measurable goals.

Example:

✔ Solve 50 SQL Problems

✔ Complete 2 Kaggle datasets

✔ Build 1 Flask Project

Expected Outcome

Write ONLY one professional paragraph explaining what the student will achieve after completing Phase 1.

Phase 2 (1-3 Months)

Create four subsections.

Technical Skills
• ...

Projects
• ...

Certifications
• ...

Outcome
• ...

Phase 3 (3-6 Months)

Create four subsections.

Advanced Skills
• ...

Projects
• ...

Deployment & Cloud
• ...

Outcome
• ...

Recommended Certifications:

Recommend only internationally recognized certifications.

For every certification provide:

Certification Name

Provider

One-line reason why it is valuable.

Important Advice:

Generate 6-8 professional career recommendations.

Focus on:

• GitHub
• LinkedIn
• Portfolio
• Open Source
• Kaggle
• Hackathons
• SQL
• Interview Preparation
• Networking
• Continuous Learning

IMPORTANT RULES

1. Never repeat resume content.

2. Never print Resume.

3. Never print Skills.

4. Never print Projects.

5. Never print Education.

6. Never print Contact Details.

7. Never mention that you analyzed the resume.

8. Never use markdown.

9. Never use **

10. Never use ##

11. Never use #

12. Make the language premium, concise, professional and industry-oriented.

13. Personalize every recommendation based on the candidate's resume.

14. Start directly from Current Level.

"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    text = response.choices[0].message.content
    if "Resume" in text:
        text = text.split("Resume")[0]

    if "PROFILE SUMMARY" in text:
        text = text.split("PROFILE SUMMARY")[0]

    text = text.replace("**", "")
    text = text.replace("##", "")
    text = text.replace("#", "")

    text = text.replace(
        "Current Level:",
        "<b style='color:#7C3AED;'>🎯 Current Level:</b>"
    )

    text = text.replace(
        "Career Goal:",
        "<b style='color:#7C3AED;'>💼 Career Goal:</b>"
    )

    text = text.replace(
        "Phase 1",
        "<b style='color:#7C3AED;'>📚 Phase 1</b>"
    )

    text = text.replace(
        "Phase 2",
        "<b style='color:#7C3AED;'>🚀 Phase 2</b>"
    )

    text = text.replace(
        "Phase 3",
        "<b style='color:#7C3AED;'>🏆 Phase 3</b>"
    )

    text = text.replace(
        "Technical Skills",
        "<div style='margin-top:18px;margin-bottom:8px;font-size:18px;font-weight:700;color:#2563EB;'>💻 Technical Skills</div>"
    )

    text = text.replace(
        "Projects",
        "<div style='margin-top:18px;margin-bottom:8px;font-size:18px;font-weight:700;color:#7C3AED;'>🚀 Projects</div>"
    )

    text = text.replace(
        "Practice Goals",
        "<div style='margin-top:18px;margin-bottom:8px;font-size:18px;font-weight:700;color:#F97316;'>🎯 Practice Goals</div>"
    )

    text = text.replace(
        "Expected Outcome",
        "<div style='margin-top:18px;margin-bottom:10px;font-size:18px;font-weight:700;color:#16A34A;'>🎯 Expected Outcome</div>"
    )

    text = text.replace(
        "Advanced Skills",
        "<div style='margin-top:18px;margin-bottom:8px;font-size:18px;font-weight:700;color:#DC2626;'>🧠 Advanced Skills</div>"
    )

    text = text.replace(
        "Deployment & Cloud",
        "<div style='margin-top:18px;margin-bottom:8px;font-size:18px;font-weight:700;color:#0891B2;'>☁️ Deployment & Cloud</div>"
    )

    text = text.replace(
        "Certifications",
        "<div style='margin-top:18px;margin-bottom:8px;font-size:18px;font-weight:700;color:#CA8A04;'>📜 Certifications</div>"
    )

    text = re.sub(
        r"(Recommended|Suggested|Professional)\s+Certifications:?",
            """
<div style="text-align:center; margin:18px 0;">

<div style="
    display:inline-flex;
    align-items:center;
    justify-content:center;
    gap:12px;
    min-width:480px;
    height:60px;
    padding:0 28px;
    background:linear-gradient(90deg,#7C3AED,#A855F7);
    color:white;
    font-size:21px;
    font-weight:700;
    border-radius:16px;
    box-shadow:0 8px 20px rgba(124,58,237,.25);
">
🎓 <span>RECOMMENDED CERTIFICATIONS</span>
</div>

</div>
""",
            text,
            flags=re.IGNORECASE,
    )
    text = re.sub(
        r"(Important|Final|Career)\s+Advice:?",
        """
<div style="text-align:center; margin:18px 0;">

<div style="
    display:inline-flex;
    align-items:center;
    justify-content:center;
    gap:12px;
    min-width:380px;
    height:60px;
    padding:0 28px;
    background:linear-gradient(90deg,#16A34A,#22C55E);
    color:white;
    font-size:21px;
    font-weight:700;
    border-radius:16px;
    box-shadow:0 8px 20px rgba(34,197,94,.25);
">
💡 <span>IMPORTANT ADVICE</span>
</div>

</div>
""",
        text,
        flags=re.IGNORECASE,
    )

    # Beautify checkmarks
    text = text.replace("✔", "✅ ")
    text = text.replace("•", "🔹 ")
    text = text.replace("\n", "<br>")
    print(text)
    return text