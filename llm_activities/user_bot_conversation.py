import google.generativeai as genai
import json
import os
from dotenv import load_dotenv
import datetime
load_dotenv(".env")


def extract_date_time(chat_history: list, date_and_time: str):
    try:
        print(
            f"Generating response for query: {chat_history} with answer type: {date_and_time}"
        )
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel(
            model_name=os.environ.get("GEMINI_MODEL"),
            system_instruction=f"""You are an Advanced AI capable of extracting date and time from the user chats.\
           Based on the data you need to extract the date and time user wants to schedule a meeting or if date and time not given then ask the user about date and time.\
            Here are some of the examples of such chats- 

            1) I need to meet for 45 minutes sometime before my flight that leaves on Friday at 6 PM.\
            2) Can we schedule a 1-hour meeting for the last weekday of this month?\
            3) I'm free sometime next week, but not too early in the morning and not on Wednesday.\
            4) Find a time in the evening, maybe after 7, but I need at least an hour to decompress after my last meeting of the day.\
            5)I have 9:30 AM or 11:00 AM available.

            Now, we need to understand the user inputs and based on that we will either ask for date or time or we will extract it.

            If date and time can be extracted then return answer in JSON format with two keys - date and time.\
            Else current context is not sufficient the return answer in JSON format with one key - insuffficient_context with value as - "need more context".\
                
                do not use json word in response.\
                The user chat history is: {chat_history}
                present date and time: {date_and_time}""",
            generation_config={"response_mime_type": "application/json"},
        )
        response = model.generate_content(chat_history)
        response = json.loads(response.text)
        print(response)
        # return response["casual"], response["formal"]
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I couldn't generate a response at this time."

now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
chat_history = [
    "how are you?",
     "I need to meet for 45 minutes sometime before my flight that leaves on Friday at 6 PM",
     "have some plans for today.",
     "need to check fot some other day."
]


# build 2 more llms, one for asking about the data and time if not present and other for finally approval
def find_and_select_avlbl_slot():
    pass

def approve_the_slot():
    pass

extract_date_time(chat_history, now)
