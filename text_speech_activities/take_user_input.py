"""
module for taking voice inputs from users."""
import speech_recognition as sr

def listen_to_user( ):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source, timeout=60, phrase_time_limit=60)
        try:
            user_input = recognizer.recognize_google(audio)
            print(f"User: {user_input}")
            return user_input
        except sr.UnknownValueError:
            print(" ")
        except sr.RequestError:
            print("Could not request results from the speech recognition service.")
            return ""
