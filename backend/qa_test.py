import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()

print("🎤 Speak now...")

with mic as source:
    r.adjust_for_ambient_noise(source, duration=0.5)
    audio = r.listen(source)

try:
    text = r.recognize_google(audio)
    print("📝 You said:", text)
except:
    print("❌ Could not recognize speech")
