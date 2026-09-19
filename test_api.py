import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = "https://api.nugen.in/api/v3/inference/chat/completions"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('API_KEY')}",
    "Content-Type": "application/json"
}

payload = {
    "model": "qwen-v2p5-0p5b-instruct",
    "messages": [
        {
            "role": "user",
            "content": "Explain what a Data Scientist does in simple terms."
        }
    ],
    "max_tokens": 300,
    "temperature": 0.1,
    "stream": False
}

response = requests.post(
    url,
    headers=headers,
    json=payload
)

print("Status:", response.status_code)
print(response.text)