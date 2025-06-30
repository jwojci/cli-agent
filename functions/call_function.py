from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_files_content import get_file_content, schema_get_file_content
from functions.run_python import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

from google.genai import types
from config import WORKING_DIR

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    if verbose:
        print(f"Calling function: {function_name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_name}")

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    if function_name in function_map.keys():
        try:
            function_result = function_map[function_name](
                WORKING_DIR, **function_call_part.args
            )
            response_data = {"result": function_result}
        except Exception as e:
            response_data = {
                "error": f"Function {function_name} failed with error: {type(e).__name__}: {e}"
            }
    else:
        response_data = {"error": f"Unknown function: {function_name}"}

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name, response=response_data
            )
        ],
    )
