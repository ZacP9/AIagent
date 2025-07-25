import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys


load_dotenv()

def main():
    print("Hello from aiagent!")
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("Error: Content argument is required")
        sys.exit(1)

    verbose = "--verbose" in sys.argv
    if verbose:
        sys.argv.remove("--verbose")  # Remove it so content is still argv[1]
    
    content = sys.argv[1]
    
    if verbose:
        print(f"User prompt: {content}")

    content = sys.argv[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=content)]),
    ]
    response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    )
    print(response.text)
    
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()

