import os
from google.genai import types

def write_file(working_directory, file_path, content):
    wd_abs = os.path.abspath(working_directory)
    file_path_abs = os.path.abspath(os.path.join(wd_abs, file_path))
    if not (file_path_abs == wd_abs or file_path_abs.startswith(wd_abs + os.sep)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        os.makedirs(os.path.dirname(file_path_abs), exist_ok=True)
        with open(file_path_abs, "w") as f:
            f.write(content)
    except Exception as e:
        return f'Error: {e}'
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the given content to the file at the given file path in the working directory, creating the file first if it does not already exist. Returns a success message with the number of characters written on success.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write to (or create and then write to, if necessary), relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content string to be written to the destination file.",
            ),
        },
    ),
)