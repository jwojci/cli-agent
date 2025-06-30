import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from functions.call_function import call_function, available_functions

MAX_ITERS = 20


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

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

        if "<plan>" in response_text:
            print("Agent has a plan:")
            plan_start = response_text.find("<plan>") + len("<plan>")
            plan_end = response_text.find("</plan>")
            plan = response_text[plan_start:plan_end].strip()
            print(plan)

            user_input = (
                input("\nProceed with this plan? (y/n/r for revise): ").strip().lower()
            )
            if user_input == "y":
                print("Plan approved. Proceeding with execution...")
                messages.append(
                    types.Content(
                        role="user", parts=[types.Part(text="Proceed with the plan.")]
                    )
                )
                continue

            elif user_input == "r":
                # get reason and ask for a new plan
                reason = input("Please provide your feedback for revision: ")
                feedback_prompt = (
                    f"The user has rejected the previous plan. "
                    f"Here is their feedback: '{reason}'.\n\n"
                    f"Please analyze this feedback and generate a new plan."
                )
                messages.append(
                    types.Content(role="user", parts=[types.Part(text=feedback_prompt)])
                )
                continue  # Go to the next iteration to get a revised plan

            else:
                print("Plan rejected. Exiting.")
                break

        if function_calls:
            function_responses = []
            for function_call_part in function_calls:
                function_call_result = call_function(function_call_part, verbose)
                if (
                    not function_call_result.parts
                    or not function_call_result.parts[0].function_response
                ):
                    raise Exception("empty function call result")
                if verbose:
                    print(
                        f"-> {function_call_result.parts[0].function_response.response}"
                    )
                function_responses.append(function_call_result.parts[0])

            if not function_responses:
                raise Exception("no function responses generated, exiting.")

            messages.append(types.Content(role="tool", parts=function_responses))
            continue

        if response_text:
            print("\nFinal Answer:")
            print(response_text)
            break

        print("No actionable response from the model. Exiting.")
        break

    if iters >= MAX_ITERS:
        print(f"Maximum iterations ({MAX_ITERS}) reached.")
        sys.exit(1)


if __name__ == "__main__":
    main()
