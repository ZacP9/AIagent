import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.function_declarations import *
from functions.call_function import call_function


load_dotenv()

def main():
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

    content = sys.argv[1]

    api_key = os.environ.get("GEMINI_API_KEY")
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

    response = client.models.generate_content(
    model = model_name,
    contents = messages,
    config = types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt),
    )

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

 
if __name__ == "__main__":
    main()
