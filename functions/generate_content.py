from google import genai
from google.genai import types
from functions.call_function import call_function

def generate_content(client, model_name, messages, functions, system_prompt, verbose):    
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[functions], system_instruction=system_prompt
        ),
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)
    
    # If AI provided text response (no function calls), return it as final answer
    if not response.function_calls:
        return response.text

    # If AI made function calls, execute them and return None (continue iterating)
    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)

        # Validate the result
        if (
            not function_call_result.parts or
            not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        
        # Collect the result
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    # Add function results to conversation and return None (implicit)
    # This signals to the main loop to continue with another iteration
    messages.append(types.Content(role="tool", parts=function_responses))

    return None  # Explicit: function calls executed, continue iterating