# def listen_question():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("🎤 Listening...")
#         audio = r.listen(source, timeout=3, phrase_time_limit=6)

#     try:
#         return r.recognize_google(audio)
#     except:
#         return None

import speech_recognition as sr

def listen_question(timeout=5):
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("🎤 Listening for audience question...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=timeout)

        question = r.recognize_google(audio)
        return question

    except sr.WaitTimeoutError:
        print("⏱ No speech detected")
        return ""

    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return ""

    except sr.RequestError as e:
        print("⚠ Speech service error:", e)
        return ""
