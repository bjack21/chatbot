import os
import json

# Ensure SERVICE_TOKEN matches .env or session
os.environ.setdefault("SERVICE_TOKEN", "chatbot-secure-token-2025")

# Create a dummy OpenAI client that mimics the response shape
class DummyChoice:
    def __init__(self, content):
        self.message = {"content": content}

class DummyResponse:
    def __init__(self, content):
        self.choices = [DummyChoice(content)]

class DummyChat:
    class completions:
        @staticmethod
        def create(model, messages, max_tokens, temperature):
            prompt = messages[0]["content"] if messages else ""
            # return a simple echoed response for testing
            return DummyResponse(f"# Generated (mock)\n# model={model}\n# prompt={prompt}\ndef mock():\n    return 'hello'\n")

class DummyOpenAI:
    def __init__(self, api_key=None):
        self.api_key = api_key
    @property
    def chat(self):
        return DummyChat()

# Import the web app and monkeypatch the OpenAI class
import web
web.OpenAI = DummyOpenAI

app = web.app

with app.test_client() as client:
    # Health
    r = client.get('/health')
    print('health', r.status_code, r.get_json())

    # Generate (authorized)
    headers = {'Authorization': 'Bearer chatbot-secure-token-2025'}
    payload = {'prompt': 'Write a Python function that adds two numbers'}
    r = client.post('/generate', headers=headers, json=payload)
    print('/generate', r.status_code)
    try:
        print(json.dumps(r.get_json(), indent=2))
    except Exception:
        print(r.data)

    # Generate (unauthorized)
    r = client.post('/generate', headers={}, json=payload)
    print('/generate (no auth)', r.status_code, r.get_json())
