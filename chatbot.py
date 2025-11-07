import os
import sys
from openai import OpenAI, OpenAIError


def get_api_key():
    """Retrieve API key from OPENAI_API_KEY env var or prompt the user.

    Note: It's more secure to set the OPENAI_API_KEY environment variable
    rather than entering it interactively.
    """
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        return key
    try:
        # Prompt user if env var not set (safer to set env var in production)
        key = input("Enter your OpenAI API key (or set OPENAI_API_KEY): ").strip()
    except (EOFError, KeyboardInterrupt):
        return None
    return key or None


def generate_code(prompt, model="gpt-4o-mini", max_tokens=300, temperature=0.2, client=None):
    """Call OpenAI ChatCompletion and return the assistant's message content.

    Returns a string with an error message on failure.
    """
    if client is None:
        api_key = get_api_key()
        if not api_key:
            return "[Error] No API key available"
        client = OpenAI(api_key=api_key)
        
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        # Be defensive: ensure choices exist and have the expected shape
        if (
            not hasattr(response, "choices")
            or len(response.choices) == 0
            or not hasattr(response.choices[0], "message")
        ):
            return "[Error] Unexpected API response format."
        return response.choices[0].message.get("content", "")
    except OpenAIError as e:
        return f"[Error] OpenAI API error: {e}"
    except Exception as e:
        return f"[Error] Unexpected error: {e}"


def main():
    api_key = get_api_key()
    if not api_key:
        print("No API key provided. Set OPENAI_API_KEY or provide one interactively.")
        sys.exit(1)
    client = OpenAI(api_key=api_key)

    print("AI Code Chatbot. Type 'exit' to quit.")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
        if not user_input:
            # ignore empty input
            continue
        if user_input.lower() == "exit":
            break
        code = generate_code(user_input)
        print("\nBot generated code:\n")
        print(code)
        print("\n" + ("-" * 60) + "\n")


if __name__ == "__main__":
    main()