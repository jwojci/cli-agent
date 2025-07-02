import os
import sys
import re

from dotenv import load_dotenv
from google import genai
from google.genai import types

import tui
from prompts import system_prompt
from functions.call_function import call_function, available_functions

MAX_ITERS = 20


def extract_content(text: str, tag: str) -> str | None:
    """Extracts content from between specified XML tags."""
    pattern = f"<{tag}>(.*?)</{tag}>"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else None


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        tui.display_greeting()
        sys.exit(0)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        tui.display_error("GEMINI_API_KEY not found in .env file.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    user_prompt = " ".join(args)
    tui.display_user_prompt(user_prompt)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    iters = 0
    while iters < MAX_ITERS:
        iters += 1

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
        except Exception as e:
            print(f"Error generating content: {e}")
            break

        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        if not response.candidates:
            print("No response from model. Exiting")
            break

        candidate_content = response.candidates[0].content
        messages.append(candidate_content)

        response_text = (
            candidate_content.parts[0].text
            if candidate_content.parts and candidate_content.parts[0].text
            else ""
        )
        function_calls = response.function_calls

        plan = extract_content(response_text, "plan")
        reflection = extract_content(response_text, "reflection")

        if reflection:
            tui.display_reflection(reflection)

        if plan:
            tui.display_plan(plan)
            user_input = tui.get_confirmation(
                "Proceed with this plan? (y/n/r for revise)"
            )
            if user_input == "y":
                messages.append(
                    types.Content(
                        role="user", parts=[types.Part(text="Proceed with the plan.")]
                    )
                )
                continue
            elif user_input == "r":
                reason = tui.console.input(
                    "[bold]Please provide your feedback for revision: [/bold]"
                )
                feedback = f"The user has rejected the plan. Feedback: '{reason}'. Generate a new plan."
                messages.append(
                    types.Content(role="user", parts=[types.Part(text=feedback)])
                )
                continue
            else:
                tui.display_error("Plan rejected by user. Exiting.")
                break

        if function_calls:
            for function_call_part in function_calls:
                tui.display_function_call(
                    function_call_part.name, dict(function_call_part.args)
                )
                function_result = call_function(function_call_part, verbose)
                response_payload = function_result.parts[0].function_response
                tui.display_function_response(dict(response_payload.response))
                messages.append(function_result)
            continue

        final_answer = response_text
        if plan or reflection:
            if not final_answer.strip():
                continue

        if final_answer:
            tui.display_final_answer(final_answer)
            break

        tui.display_error("No actionable response from the model. Exiting.")
        break

    if iters >= MAX_ITERS:
        tui.display_error(f"Maximum iterations ({MAX_ITERS}) reached.")
        sys.exit(1)


if __name__ == "__main__":
    main()
