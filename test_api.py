import os
import requests
import json

BASE = os.environ.get("BASE_URL", "http://127.0.0.1:5000")
TOKEN = os.environ.get("SERVICE_TOKEN", "chatbot-secure-token-2025")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

print("Testing health endpoint...")
resp = requests.get(f"{BASE}/health")
print(resp.status_code, resp.text)

print("Testing generate endpoint...")
body = {"prompt": "Write a Python function that adds two numbers"}
resp = requests.post(f"{BASE}/generate", headers=HEADERS, json=body)
print(resp.status_code)
try:
    print(json.dumps(resp.json(), indent=2))
except Exception:
    print(resp.text)
