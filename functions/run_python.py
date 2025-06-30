import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path):
    cwd_abs_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(cwd_abs_path, file_path))

    if not abs_file_path.startswith(cwd_abs_path + os.sep):
        raise PermissionError(
            f'Cannot execute "{file_path}" as it is outside the permitted working directory'
        )

    if not os.path.isfile(abs_file_path):
        raise FileNotFoundError(f'File "{file_path}" not found.')

    if not file_path.endswith(".py"):
        raise ValueError(f'Error: "{file_path}" is not a Python file.')

    try:
        completed_process = subprocess.run(
            ["python", abs_file_path],
            timeout=30,
            cwd=cwd_abs_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return_string = (
            f"STDOUT:\n{completed_process.stdout}\nSTDERR:\n{completed_process.stderr}"
        )
        if completed_process.returncode != 0:
            return_string += f"\nProcess exited with non-zero return code: {completed_process.returncode}"
        return return_string
    except subprocess.TimeoutExpired:
        raise TimeoutError("Python script execution timed out after 30 seconds.")
    except Exception as e:
        raise OSError(f"Error executing Python file '{file_path}': {e}")


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Filepath of the python script to run",
            )
        },
        required=["file_path"],
    ),
)
