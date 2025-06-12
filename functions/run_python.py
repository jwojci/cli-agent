import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path):
    cwd_abs_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(cwd_abs_path, file_path))

    if not abs_file_path.startswith(cwd_abs_path + os.sep):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(
            ["python", abs_file_path],
            timeout=30,
            cwd=cwd_abs_path,
            capture_output=True,
            text=True,
        )
        return_string = """"""
        return_string += str(f"STDOUT:{completed_process.stdout}")
        return_string += str(f"STDERR:{completed_process.stderr}")
        return_code = completed_process.returncode
        if return_code != 0:
            return_string += f"Process exited with code {return_code}"
        if completed_process.stdout is None:
            return "No output produced."
        return str(return_string)
    except Exception as e:
        return f"Error: executing Python file: {e}"


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
    ),
)
