import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_projects(resume_text):

    prompt = f"""
You are an AI Career Mentor.

Read the candidate's resume carefully.

Suggest exactly 5 NEW portfolio projects.

Rules:

- Do NOT repeat projects already present in the resume.
- Recommend projects suitable for the candidate's current skill level.
- For each project provide:

1. Project Name
2. Difficulty
3. Skills Learned
4. Short Description

Resume:

{resume_text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    text = response.choices[0].message.content

    # Remove Markdown
    text = text.replace("###", "")
    text = text.replace("##", "")
    text = text.replace("#", "")
    text = text.replace("**", "")
    text = text.replace("* ", "• ")

    # Highlight headings
    text = text.replace(
        "Project Name:",
        "<b style='color:#7C3AED;'>📌 Project Name:</b>"
    )

    text = text.replace(
        "Difficulty:",
        "<b style='color:#7C3AED;'>📊 Difficulty:</b>"
    )

    text = text.replace(
        "Skills Learned:",
        "<b style='color:#7C3AED;'>🛠 Skills Learned:</b>"
    )

    text = text.replace(
        "Short Description:",
        "<b style='color:#7C3AED;'>📝 Short Description:</b>"
    )

    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")

    return text