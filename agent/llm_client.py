import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key or api_key == "paste_your_actual_key_here":
    raise RuntimeError(
        "GROQ_API_KEY is missing. Add your real key to the .env file."
    )

client = Groq(api_key=api_key)
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")


def ask_groq(message: str) -> str:
    """Send a user message to Groq and return its text response."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Linux process ancestry assistant. "
                    "Help users understand processes, PIDs, parent PIDs, "
                    "and process ancestry. Do not invent process information."
                ),
            },
            {"role": "user", "content": message},
        ],
    )

    return response.choices[0].message.content or ""
