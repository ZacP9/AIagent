import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.function_declarations import *
from functions.generate_content import generate_content
from config import MAX_ITERS


def main():
    load_dotenv()
    print("Hello from aiagent!")

    if len(sys.argv) < 2:
        print("Error: Content argument is required")
        sys.exit(1)

    verbose = "--verbose" in sys.argv
    if verbose:
        sys.argv.remove("--verbose")  # Remove it so content is still argv[1]
    
    content = sys.argv[1]
    
    if verbose:
        print(f"User prompt: {content}")

    # Check for API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is required")
        sys.exit(1)
        
    client = genai.Client(api_key=api_key)

    model_name = "gemini-2.0-flash-001"
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=content)]),
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)

        try:
            result = generate_content(client, model_name, messages=messages, functions=available_functions, system_prompt=system_prompt, verbose=verbose)
            
            if result is None:
                # AI made function calls but didn't provide text response yet
                if verbose:
                    print(f"Iteration {iters}: Function calls executed, continuing...")
                continue

            else:
                # AI provided final text response
                print("Final response:")
                print(result)
                break

        except Exception as e:
            print(f"Error in generate_content: {e}")

    
if __name__ == "__main__":
    main()
