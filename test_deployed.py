import os
import requests
import json

# Replace this with your Render URL
RENDER_URL = "https://chatbot-xxxx.onrender.com"  # Update this!
SERVICE_TOKEN = "chatbot-secure-token-2025"

def test_health():
    response = requests.get(f"{RENDER_URL}/health")
    print("Health check response:", response.text)
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_generate():
    headers = {
        "Authorization": f"Bearer {SERVICE_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": "Write a hello world program in Python",
        "max_tokens": 100
    }
    response = requests.post(
        f"{RENDER_URL}/generate",
        headers=headers,
        json=data
    )
    print("Generate response:", response.text)
    assert response.status_code == 200
    assert "completion" in response.json()

if __name__ == "__main__":
    # Update the URL before running tests
    if "xxxx" in RENDER_URL:
        print("Please update the RENDER_URL in the script with your actual Render URL!")
        exit(1)
    
    print("Testing health endpoint...")
    test_health()
    print("✅ Health check passed!\n")
    
    print("Testing generate endpoint...")
    test_generate()
    print("✅ Generate endpoint test passed!")