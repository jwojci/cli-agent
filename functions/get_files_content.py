import os
from google.genai import types
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    cwd_abs_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(cwd_abs_path, file_path))

    if not abs_file_path.startswith(cwd_abs_path + os.sep):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        content = ""
        with open(abs_file_path, "r") as f:
            content = f.read(MAX_CHARS)

        if len(content) >= 10000:
            content += '[...File "{file_path}" truncated at 10000 characters]'

        return content
    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file and outputs it.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Filepath to the file of which content to read.",
            )
        },
    ),
)
