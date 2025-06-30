import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    cwd_abs_path = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, directory))

    if not target_dir.startswith(cwd_abs_path):
        raise PermissionError(
            f'Cannot list "{directory}" as it is outside the permitted working directory'
        )
    if not os.path.isdir(target_dir):
        raise NotADirectoryError(f'Error: "{directory}" is not a directory')

    try:
        files = os.scandir(target_dir)
        files_info = "".join(
            f"- {f.name}: file_size={f.stat().st_size} bytes, is_dir={f.is_dir()}\n"
            for f in files
        )
        return files_info if files_info else "The directory is empty."
    except Exception as e:
        raise IOError(f"Error listing files in '{directory}': {e}")


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
