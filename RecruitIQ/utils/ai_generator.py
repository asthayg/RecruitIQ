import os
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_interview_questions(resume_text):

    prompt = f"""
You are a Senior HR Recruiter.

Read the resume carefully.

Generate ONLY in the following format.

TECHNICAL INTERVIEW QUESTIONS

1.
2.
3.
4.
5.
6.
7.
8.
9.
10.

HR INTERVIEW QUESTIONS

1.
2.
3.
4.
5.

IMPORTANT

- Do NOT use markdown.
- Do NOT use #.
- Do NOT use ##.
- Do NOT use ###.
- Do NOT use **.
- Do NOT use bullets.
- Return clean plain text only.

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

    # Remove markdown
    text = text.replace("###", "")
    text = text.replace("##", "")
    text = text.replace("#", "")
    text = text.replace("**", "")

    # Technical Heading
    text = re.sub(
        r"TECHNICAL\s*INTERVIEW\s*QUESTIONS:?",
        """
<div style="
width:fit-content;
margin:25px auto;
padding:14px 30px;
background:linear-gradient(90deg,#2563EB,#3B82F6);
color:white;
border-radius:15px;
font-size:22px;
font-weight:700;
box-shadow:0 10px 25px rgba(37,99,235,.30);
">
💻 TECHNICAL INTERVIEW QUESTIONS
</div>
""",
        text,
        flags=re.IGNORECASE
    )

    # HR Heading
    text = re.sub(
        r"HR\s*INTERVIEW\s*QUESTIONS:?",
        """
<div style="
width:fit-content;
margin:30px auto;
padding:14px 30px;
background:linear-gradient(90deg,#EC4899,#F472B6);
color:white;
border-radius:15px;
font-size:22px;
font-weight:700;
box-shadow:0 10px 25px rgba(236,72,153,.30);
">
👥 HR INTERVIEW QUESTIONS
</div>
""",
        text,
        flags=re.IGNORECASE
    )

    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")

    return text