from dotenv import load_dotenv
from google import genai
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.call_function import call_function
import os
import sys
def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    system_prompt = system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
    )
    if len(sys.argv) <= 1:
        print("No input provided")
        sys.exit(1)
    else:
        user_prompt = sys.argv[1]
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    iterations = 0
    while iterations <= 20:
        try:
            response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
            )
            for candidate in response.candidates or []:
                    messages.append(candidate.content)
            if response.function_calls:
                tool_parts = []
                for function_call_part in response.function_calls:
                    content = call_function(function_call_part)
                    if not content.parts[0].function_response.response:
                        raise Exception("BLEARGH!")
                    tool_parts.append(content.parts[0])
                if tool_parts:
                    messages.append(types.Content(role="user", parts=tool_parts))
            if (not response.function_calls) and response.text:
                print(response.text)
                break
            iterations += 1
        except Exception as e:
            print(f"Error: {e}")
    if "--verbose" in sys.argv:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if response.function_calls:
            print(f"-> {content.parts[0].function_response.response}")

if __name__ == "__main__":
    main()
