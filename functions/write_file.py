import os
from google.genai import types


def write_file(working_directory, file_path, content):
    cwd_abs_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(cwd_abs_path, file_path))

    if not abs_file_path.startswith(cwd_abs_path + os.sep):
        raise PermissionError(
            f'Cannot write to "{file_path}" as it is outside the permitted working directory'
        )

    try:
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        with open(abs_file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        raise IOError(f"Could not write to file '{file_path}': {e}")


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Filepath of the file that is being written to",
            ),
            "content": types.Schema(
                type=types.Type.STRING, description="Content to write to the file"
            ),
        },
        required=["file_path", "content"],
    ),
)
