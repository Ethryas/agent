import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    wd_abs = os.path.abspath(working_directory)
    file_path_abs = os.path.abspath(os.path.join(wd_abs, file_path))
    if not (file_path_abs == wd_abs or file_path_abs.startswith(wd_abs + os.sep)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(file_path_abs):
        return f'Error: File "{file_path}" not found.'
    if not file_path_abs.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    result_object = subprocess.run(["python", file_path_abs, *args], timeout=30, capture_output=True, text=True, cwd=wd_abs)
    try:
        exit_code = result_object.returncode
        if exit_code != 0:
            return f"STDOUT: {result_object.stdout}, STDERR: {result_object.stderr}. Process exited with code {exit_code}"
        if len(result_object.stdout) == 0 and len(result_object.stderr) == 0:
            return "No output produced."
        return f'STDOUT: {result_object.stdout}, STDERR: {result_object.stderr}'
    except Exception as e:
        print(f'Error: {e}')

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Attempts to run the given Python file, located in the working directory, capturing and returning the output STDOUT and STDERR and exit code as text",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to run in Python, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="A list of args to be unpacked by the subprocess function.",
            )
        },
    ),
)