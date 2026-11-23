
import os
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found!")

client = genai.Client(api_key=api_key)


def ask_gemini(prompt):

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except errors.APIError as e:

        if e.code == 503:
            print("Gemini is temporarily overloaded.")
            print("Please try again in a few minutes.")

        else:
            print(f"Gemini API error: {e}")

        return None
