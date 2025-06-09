import openai
import speech_recognition as sr
import pyttsx3
import datetime
import csv
import os

# 🔑 Replace with your API key
openai.api_key = "your_openai_api_key"

# 🗣️ Text-to-speech engine setup
engine = pyttsx3.init()
def speak(text):
    print("🤖:", text)
    engine.say(text)
    engine.runAndWait()

# 🎤 Listen to voice input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Speak something...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("👤:", text)
        return text
    except:
        speak("Sorry, I didn't catch that.")
        return ""

# 🧠 Get AI response
def get_ai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or gpt-4 if available
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# 📝 Track learning progress locally
def log_progress(prompt, response):
    today = datetime.date.today().isoformat()
    file_exists = os.path.exists("cybercoach_log.csv")
    with open("cybercoach_log.csv", "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Question", "Answer"])
        writer.writerow([today, prompt, response])

# 🚀 Main Assistant Loop
def start_assistant():
    speak("Welcome back to CyberCoachAI. Ask me anything about Python or cybersecurity.")
    while True:
        query = listen()
        if "exit" in query.lower():
            speak("Goodbye. Keep learning.")
            break
        elif "what should I study" in query.lower():
            response = "Today's lesson: Practice Python lists or complete TryHackMe Module 2."
        else:
            response = get_ai_response(query)

        speak(response)
        log_progress(query, response)

if __name__ == "__main__":
    start_assistant()
      
