import tkinter as tk
from tkinter import scrolledtext
import openai
import pyttsx3
import speech_recognition as sr
import datetime
import csv

openai.api_key = "your_openai_api_key"

# Voice
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Listen to mic
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        output_box.insert(tk.END, "\n🎙️ Listening...\n")
        window.update()
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        return "Sorry, I didn't catch that."

# ChatGPT call
def get_ai_response(prompt):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return res['choices'][0]['message']['content']

# Log conversation
def log_convo(question, answer):
    with open("cybercoach_log.csv", "a", newline="") as file:
        writer = csv.writer(file)
        today = datetime.date.today().isoformat()
        writer.writerow([today, question, answer])

# Ask and respond
def ask_question():
    query = input_box.get()
    if not query.strip():
        query = listen()
    output_box.insert(tk.END, f"\n👤: {query}\n")
    answer = get_ai_response(query)
    output_box.insert(tk.END, f"🤖: {answer}\n")
    speak(answer)
    log_convo(query, answer)
    input_box.delete(0, tk.END)

# UI Setup
window = tk.Tk()
window.title("CyberCoachAI")
window.geometry("600x500")

output_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=70, height=20)
output_box.pack(padx=10, pady=10)

input_box = tk.Entry(window, width=50)
input_box.pack(padx=10, pady=5)

ask_button = tk.Button(window, text="Ask", command=ask_question)
ask_button.pack(pady=5)

mic_button = tk.Button(window, text="🎙️ Speak", command=ask_question)
mic_button.pack()

window.mainloop()
