"""
module containing all the Agentic logic like understanding the user intent and take action accordingly.
"""

import google.generativeai as genai
import json
import os
from dotenv import load_dotenv
load_dotenv(".env")


def extract_date_time(chat_history: list, date_and_time: str, upcoming_events):

    try:
        
        print("Luna: Processing your query .... give me a moment please.")
        gemini_prompt = os.environ.load("GEMINI_PROMPT")
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel(
            model_name=os.environ.get("GEMINI_MODEL"),
            system_instruction=f"""{gemini_prompt}""",
            generation_config={"response_mime_type": "application/json" },
        )
        response = model.generate_content(chat_history)
        response = json.loads(response.text)

        return {"success": True, "response": response}
    except Exception as e:
        print(f"Error generating response: {e}")
        return {
            "success": False,
            "response": {
                "llm_failure": "Sorry, I couldn't generate a response at this time."
            },
        }
