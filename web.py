import os
from flask import Flask, request, jsonify
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # dotenv not available in this environment; env vars must be set externally
    pass

from openai import OpenAI, OpenAIError

app = Flask(__name__)

# Simple service token for minimal auth. Set SERVICE_TOKEN env var on the host.
SERVICE_TOKEN = os.environ.get("SERVICE_TOKEN")


def check_auth(req):
    print(f"Checking auth with SERVICE_TOKEN: {SERVICE_TOKEN}")
    print(f"Request auth header: {req.headers.get('Authorization', '')}")
    
    if not SERVICE_TOKEN:
        print("No SERVICE_TOKEN configured")
        return False
    
    auth = req.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        print("Missing Bearer prefix")
        return False
    
    token = auth.split(" ", 1)[1]
    result = token == SERVICE_TOKEN
    print(f"Token match result: {result}")
    return result


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/generate", methods=["POST"])
def generate():
    print("Received request to /generate")
    print(f"Headers: {request.headers}")
    
    # Basic token check
    if not check_auth(request):
        print("Auth failed")
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json() or {}
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "missing 'prompt' in JSON body"}), 400

    # Optional params (with safe defaults)
    model = data.get("model", "gpt-4o-mini")
    try:
        max_tokens = int(data.get("max_tokens", 300))
    except Exception:
        max_tokens = 300
    try:
        temperature = float(data.get("temperature", 0.2))
    except Exception:
        temperature = 0.2

    # Create OpenAI client
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return jsonify({"error": "server misconfigured: OPENAI_API_KEY not set"}), 500

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        # Extract message content robustly (support dicts or objects)
        choice = response.choices[0]
        msg = getattr(choice, "message", None)
        if msg is None and isinstance(choice, dict):
            msg = choice.get("message")
        content = None
        if isinstance(msg, dict):
            content = msg.get("content")
        elif hasattr(msg, "content"):
            content = msg.content
        # Fallbacks for other possible shapes
        if content is None:
            # try older response shape
            try:
                content = response.choices[0]["message"]["content"]
            except Exception:
                content = None
        if content is None:
            return jsonify({"error": "Unexpected API response format."}), 500
        return jsonify({"code": content})
    except OpenAIError as e:
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


if __name__ == "__main__":
    # Local development server (not for production)
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting server on port {port}...")
    # Disable Flask reloader here to keep a single stable process when started
    app.run(host="0.0.0.0", port=port, debug=False)
