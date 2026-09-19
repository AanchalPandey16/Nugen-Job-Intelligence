import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

BASE_URL = "https://api.nugen.in/api/v3/inference/chat/completions"

BASE_MODEL = "llama-v3p2-3b-reasoning"
V1_MODEL = "model_01m2qxph26qmrzmp"
V2_MODEL = "model_01m2qz57xbjdhnws"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

test_cases = [
    """
Job requires Python, SQL, FastAPI, Docker and model deployment.

Candidate resume contains:
Python, SQL, scikit-learn, FastAPI, and deployed a machine learning API.

Evaluate the candidate.
Classify skills as Matched, Partially Matched, and Missing.
Do not assume undocumented skills.
""",

    """
Job requires Python, Django, PostgreSQL and REST API development.

Candidate resume contains:
Python, FastAPI, MySQL and REST API development.

Evaluate the candidate.
Classify skills as Matched, Partially Matched, and Missing.
Do not assume that knowledge of one framework means knowledge of another.
""",

    """
Job requires Python, Machine Learning, Deep Learning, TensorFlow and NLP.

Candidate resume contains:
Python, scikit-learn, classification, regression and basic NLP projects.

Evaluate the candidate.
Classify skills as Matched, Partially Matched, and Missing.
Do not infer Deep Learning or TensorFlow unless explicitly supported.
""",

    """
Job requires SQL, Excel, Power BI and Tableau.

Candidate resume contains:
SQL, Excel, Matplotlib and Tableau.

Evaluate the candidate.
Classify skills as Matched, Partially Matched, and Missing.
Do not assume Power BI knowledge from other visualization tools.
""",

    """
Job requires Python, LLM APIs, RAG, vector databases and FastAPI.

Candidate resume contains:
Python, OpenAI API integration and FastAPI.

Evaluate the candidate.
Classify skills as Matched, Partially Matched, and Missing.
Do not invent experience.
"""
]


def call_model(model_name, prompt):
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 500,
        "temperature": 0.1,
        "stream": False
    }

    response = requests.post(
        BASE_URL,
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        return {
            "error": response.text,
            "status": response.status_code
        }

    data = response.json()

    return {
        "content": data["choices"][0]["message"]["content"],
        "confidence": data.get("confidence_score", "N/A"),
        "model": data.get("model")
    }


for i, test in enumerate(test_cases, start=1):

    print("\n")
    print("=" * 100)
    print(f"TEST CASE {i}")
    print("=" * 100)

    print("\nPROMPT:\n")
    print(test)

    models = [
        ("BASE MODEL", BASE_MODEL),
        ("V1 ALIGNED MODEL", V1_MODEL),
        ("V2 ALIGNED MODEL", V2_MODEL)
    ]

    for label, model_id in models:

        print("\n" + "-" * 100)
        print(f"\n{label} RESPONSE:\n")

        result = call_model(model_id, test)

        if "error" in result:
            print("Error:", result)
        else:
            print(result["content"])
            print("\nConfidence:", result["confidence"])
            print("Model:", result["model"])