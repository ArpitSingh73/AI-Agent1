"""
module for taking voice inputs from users."""
import speech_recognition as sr

def listen_to_user( ):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print( "User ....  ")
        # convert_text_to_speech(" listening... Please speak.")
        audio = recognizer.listen(source, timeout=60, phrase_time_limit=60)
        try:
            user_input = recognizer.recognize_google(audio)
            print(f"User: {user_input}")
            return user_input
        except sr.UnknownValueError:
            print(" ")
            # convert_text_to_speech("Sorry, I could not understand the audio.")
            # return ""
        except sr.RequestError:
            print("Could not request results from the speech recognition service.")
            return ""
