import os
from google.genai import types


def get_files_info(working_directory, directory=None):
    cwd_abs_path = os.path.abspath(working_directory)
    target_dir = cwd_abs_path
    if directory:
        target_dir = os.path.abspath(os.path.join(working_directory, directory))
    if not target_dir.startswith(cwd_abs_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    try:
        files_info = """"""
        for f in os.scandir(os.path.join(cwd_abs_path, directory)):
            files_info += f"- {f.name}: file_size={os.path.getsize(f)} bytes, is_dir={f.is_dir()}\n"

        return files_info
    except Exception as e:
        return f"Error listing files: {e}"


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
