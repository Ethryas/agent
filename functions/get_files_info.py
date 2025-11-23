import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    wd_abs = os.path.abspath(working_directory)
    absolute_directory = os.path.abspath(os.path.join(wd_abs, directory))
    if os.path.isdir(absolute_directory) == False:
        return f'Error: "{directory}" is not a directory'
    if not (absolute_directory == wd_abs or absolute_directory.startswith(wd_abs + os.sep)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    dir_contents = []
    try:
        items = os.listdir(absolute_directory)
    except Exception as e:
        return f"Error: {e}"
    for item in items:
        name = str(item)
        full_path = os.path.join(absolute_directory, item)
        try:
            size = os.path.getsize(full_path)
        except Exception as e:
            return f'Error: {e}'
        is_dir = os.path.isdir(full_path)
        dir_contents.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")
    return "\n".join(dir_contents)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)