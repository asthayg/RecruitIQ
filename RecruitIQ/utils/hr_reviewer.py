import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_hr_review(resume_text, job_text):

    prompt=f"""

You are a Senior HR Recruiter.

Analyze the resume against the Job Description.

Return ONLY in this format.

Candidate Summary:

Strengths:

Weaknesses:

Why Ranked:

Hiring Decision:

Hiring Confidence:

Reason for Hiring:

Interview Focus:

Job Description:

{job_text}

Resume:

{resume_text}

Do not use markdown.

Do not use **

Do not use ##

"""

    response=client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {

                "role":"user",

                "content":prompt

            }

        ]

    )

    return response.choices[0].message.content