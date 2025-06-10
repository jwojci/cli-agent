import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

if len(sys.argv) <= 1:
    print("ERROR. No prompt provided.")
    sys.exit(1)


# Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

user_prompt = sys.argv[1]

messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=messages,
)

prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count

print(response.text)
if len(sys.argv) > 2:
    if sys.argv[2] == "--verbose":
        print("User prompt: ", user_prompt)
        print("Prompt tokens: ", prompt_tokens)
        print("Response tokens: ", response_tokens)
