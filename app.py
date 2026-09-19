import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="Nugen Job Intelligence")

API_KEY = os.getenv("API_KEY")

BASE_URL = "https://api.nugen.in/api/v3/inference/chat/completions"
V2_MODEL = "model_01m2qz57xbjdhnws"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


class AnalyzeRequest(BaseModel):
    resume: str
    job_description: str


def normalize(text):
    return text.lower().strip()


evidence_rules = {
    "model deployment": [
        "deployed a machine learning api",
        "deployed a model",
        "deployed model",
        "deployed machine learning model",
        "deployed churn prediction api",
        "served model",
        "production api",
        "model deployment"
    ],

    "llm apis": [
        "openai api",
        "llm api",
        "language model api",
        "large language model api"
    ],

    "machine learning": [
        "scikit-learn",
        "classification",
        "regression",
        "machine learning"
    ],

    "rest api": [
        "rest api",
        "restful api",
        "api development"
    ]
}


def extract_required_skills(job_description):
    system_prompt = """
You extract required technical and professional skills from job descriptions.

Rules:
1. Return only skills explicitly required or clearly requested in the job description.
2. Do not invent skills.
3. Do not include responsibilities unless they represent an actual skill.
4. Keep skill names short and normalized.
5. Return only a comma-separated list.
6. Do not add explanations.

Example output:
Python, SQL, Docker, AWS, FastAPI, Model Deployment
"""

    payload = {
        "model": V2_MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": job_description
            }
        ],
        "max_tokens": 250,
        "temperature": 0,
        "stream": False
    }

    response = requests.post(
        BASE_URL,
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        return []

    data = response.json()

    content = data["choices"][0]["message"]["content"]

    skills = []

    for skill in content.split(","):
        cleaned = skill.strip()

        if cleaned:
            skills.append(cleaned)

    return skills


def skill_has_evidence(skill, resume):
    skill_lower = normalize(skill)
    resume_lower = normalize(resume)

    # Exact skill match
    if skill_lower in resume_lower:
        return True

    # Direct evidence rules
    if skill_lower in evidence_rules:
        for evidence in evidence_rules[skill_lower]:
            if evidence in resume_lower:
                return True

    return False


def validate_skills(required_skills, resume):
    matched = []
    missing = []

    for skill in required_skills:
        if skill_has_evidence(skill, resume):
            matched.append(skill)
        else:
            missing.append(skill)

    return matched, missing


def call_nugen(resume, job_description):
    system_prompt = """
You are a resume-to-job evaluator.

Compare the candidate resume against the job description.

Do not invent experience.

Focus on:
- matched skills
- missing skills
- partially matched skills
- short recommendations
"""

    user_prompt = f"""
JOB DESCRIPTION:

{job_description}

RESUME:

{resume}

Evaluate the candidate.
"""

    payload = {
        "model": V2_MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
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

    if response.status_code != 200:
        return {
            "error": response.text
        }

    data = response.json()

    return {
        "analysis": data["choices"][0]["message"]["content"],
        "confidence": data.get("confidence_score")
    }


@app.get("/")
def home():
    return {
        "message": "Nugen Job Intelligence API is running"
    }


@app.post("/analyze")
def analyze(request: AnalyzeRequest):

    required_skills = extract_required_skills(
        request.job_description
    )

    matched, missing = validate_skills(
        required_skills,
        request.resume
    )

    nugen_result = call_nugen(
        request.resume,
        request.job_description
    )

    recommendation = []

    for skill in missing:
        recommendation.append(
            f"Learn and build evidence for {skill} before adding it to the resume."
        )

    return {
        "required_skills": required_skills,
        "matched": matched,
        "partially_matched": [],
        "missing": missing,
        "recommendations": recommendation,
        "nugen_analysis": nugen_result.get("analysis"),
        "confidence": nugen_result.get("confidence")
    }