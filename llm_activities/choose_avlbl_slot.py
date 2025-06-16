import google.generativeai as genai
import json
import os
from dotenv import load_dotenv
import datetime
from calender_activities.check_availability import is_slot_free

load_dotenv(".env")


def find_and_select_avlbl_slot(date, start_time, end_time, chat_history):

    booked_slots = []

    now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    slot_avlbl = is_slot_free(start_time, end_time)
    if slot_avlbl:
        try:
            print(f"Generating response for query: {date} with answer type:")
            genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
            model = genai.GenerativeModel(
                model_name=os.environ.get("GEMINI_MODEL"),
                system_instruction=f"""You are an advanced AI agent capable of scheduling a meeting based on the data provided.\
                    You are provided date and time specified with user on which user wants to schedule a call and slots available to be booked.\
                    Select the most prefferd slot and let user know about it.\
                    If slot is not available or already booked then you also need to inform the user and promote to select different time or date.\
                    But if slot is empty modify the   
                        
                        present date and time: {now}
                        details of booked slots : {booked_slots}
                                """,
                generation_config={"response_mime_type": "application/json"},
            )
            response = model.generate_content(chat_history)
            response = json.loads(response.text)
            print(response)
            # return response["casual"], response["formal"]
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Sorry, I couldn't generate a response at this time."
    else:
        return {
            "success": False,
            "message": "slot is occupied, please select other slot.",
        }
