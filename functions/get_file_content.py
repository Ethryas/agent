import os
from config import CHARACTER_LIMIT
from google.genai import types

def get_file_content(working_directory, file_path):
    wd_abs = os.path.abspath(working_directory)
    file_path_abs = os.path.abspath(os.path.join(wd_abs, file_path))
    if not (file_path_abs == wd_abs or file_path_abs.startswith(wd_abs + os.sep)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(file_path_abs):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    max_chars = CHARACTER_LIMIT
    with open(file_path_abs, "r") as f:
        try:
            file_content_string = f.read(max_chars)
        except Exception as e:
            return f'Error: {e}'
        if len(file_content_string) == max_chars:
            file_content_string += f'[...File "{file_path}" truncated at {max_chars} characters]'
        return file_content_string

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the contents of a file within the working directory as a string of up to CHARACTER_LIMIT characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to read from, relative to the working directory.",
            ),
        },
    ),
)