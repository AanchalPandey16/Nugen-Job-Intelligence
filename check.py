import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

BASE_URL = "https://api.nugen.in/api/v3/inference/chat/completions"
V2_MODEL = "model_01m2qz57xbjdhnws"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

required_skills = [
    "Python",
    "SQL",
    "FastAPI",
    "Docker",
    "Model Deployment"
]

resume_text = """
Python
SQL
scikit-learn
FastAPI
Deployed a machine learning API
"""

# Some skills may be demonstrated through concrete evidence
evidence_rules = {
    "model deployment": [
        "deployed a machine learning api",
        "deployed a model",
        "model deployment",
        "deployed machine learning model"
    ],

    "llm apis": [
        "openai api",
        "llm api",
        "large language model api"
    ],

    "machine learning": [
        "scikit-learn",
        "classification",
        "regression",
        "machine learning"
    ]
}


def normalize(text):
    return text.lower().strip()


def skill_has_evidence(skill, resume):

    skill_lower = normalize(skill)
    resume_lower = normalize(resume)

    # Exact skill exists
    if skill_lower in resume_lower:
        return True

    # Check allowed direct evidence
    if skill_lower in evidence_rules:

        for evidence in evidence_rules[skill_lower]:

            if evidence in resume_lower:
                return True

    return False


def validate_skills(required, resume):

    matched = []
    missing = []

    for skill in required:

        if skill_has_evidence(skill, resume):
            matched.append(skill)

        else:
            missing.append(skill)

    return matched, missing


SYSTEM_PROMPT = """
You are a resume-to-job evaluator.

Evaluate the candidate based only on evidence explicitly
present in the resume.

Do not invent experience.

Return:

MATCHED
PARTIALLY MATCHED
MISSING
RECOMMENDATION
"""


USER_PROMPT = f"""
JOB REQUIREMENTS:

{chr(10).join(required_skills)}

RESUME:

{resume_text}

Evaluate the candidate.
"""


payload = {
    "model": V2_MODEL,

    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": USER_PROMPT
        }
    ],

    "max_tokens": 500,
    "temperature": 0,
    "stream": False
}


response = requests.post(
    BASE_URL,
    headers=headers,
    json=payload
)


print("\n" + "=" * 70)
print("NUGEN MODEL RESPONSE")
print("=" * 70)


if response.status_code == 200:

    data = response.json()

    model_response = data["choices"][0]["message"]["content"]

    print(model_response)

    print(
        "\nConfidence:",
        data.get("confidence_score", "N/A")
    )

else:

    print(
        "Nugen API Error:",
        response.status_code,
        response.text
    )


matched, missing = validate_skills(
    required_skills,
    resume_text
)


print("\n")
print("=" * 70)
print("FINAL VALIDATED RESULT")
print("=" * 70)


print("\nMATCHED")

if matched:

    for skill in matched:
        print(f"- {skill}")

else:
    print("- None")


print("\nPARTIALLY MATCHED")
print("- None")


print("\nMISSING")

if missing:

    for skill in missing:
        print(f"- {skill}")

else:
    print("- None")


print("\nRECOMMENDATION")

if missing:

    print(
        "- Learn and demonstrate:",
        ", ".join(missing),
        "before adding them as experience."
    )

else:

    print(
        "- Candidate has evidence for all required skills."
    )