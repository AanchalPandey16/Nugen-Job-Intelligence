import requests
import json

API_URL = "http://127.0.0.1:8000/analyze"

test_cases = [
    {
        "name": "Test 1",
        "resume": """
Python, SQL, FastAPI, scikit-learn.
Deployed a churn prediction API.
""",
        "job_description": """
We require Python, SQL, FastAPI, Docker, AWS, Kubernetes,
MLflow, CI/CD and Model Deployment.
"""
    },

    {
        "name": "Test 2",
        "resume": """
Python, FastAPI, MySQL and REST API development.
""",
        "job_description": """
We require Python, Django, PostgreSQL and REST API development.
"""
    },

    {
        "name": "Test 3",
        "resume": """
Python, scikit-learn, classification, regression
and one basic NLP project.
""",
        "job_description": """
We require Python, Machine Learning, Deep Learning,
TensorFlow and NLP.
"""
    },

    {
        "name": "Test 4",
        "resume": """
SQL, Excel, Tableau and Matplotlib.
""",
        "job_description": """
We require SQL, Excel, Power BI and Tableau.
"""
    },

    {
        "name": "Test 5",
        "resume": """
Python, OpenAI API integration and FastAPI.
""",
        "job_description": """
We require Python, LLM APIs, RAG, Vector Databases and FastAPI.
"""
    }
]


for case in test_cases:

    print("\n")
    print("=" * 100)
    print(case["name"])
    print("=" * 100)

    try:
        response = requests.post(
            API_URL,
            json={
                "resume": case["resume"],
                "job_description": case["job_description"]
            },
            timeout=60
        )

        print("Status:", response.status_code)

        if response.status_code == 200:
            data = response.json()

            print("\nREQUIRED SKILLS:")
            print(data.get("required_skills"))

            print("\nMATCHED:")
            print(data.get("matched"))

            print("\nPARTIALLY MATCHED:")
            print(data.get("partially_matched"))

            print("\nMISSING:")
            print(data.get("missing"))

            print("\nRECOMMENDATIONS:")
            print(data.get("recommendations"))

            print("\nCONFIDENCE:")
            print(data.get("confidence"))

            print("\nRAW NUGEN ANALYSIS:")
            print(data.get("nugen_analysis"))

        else:
            print("Error:")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print("ERROR: FastAPI backend is not running.")

    except requests.exceptions.Timeout:
        print("ERROR: Request timed out.")

    except Exception as e:
        print("ERROR:", e)