import speech_recognition as sr
import os
import webbrowser
import openai
import datetime
from config import apikey
import random

from physics_extractor import solve_question

current_steps = []
current_step_index = 0
tutor_mode = False

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt}\n" + "*"*20 + "\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256
    )

    answer = response["choices"][0]["text"]
    print(answer)
    text += answer

    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/prompt-{random.randint(1,999999)}.txt", "w") as f:
        f.write(text)


def say(text):
    os.system(f'say "{text}"')


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language="en-IN")
        print("User said:", query)
        return query.lower()
    except Exception:
        return ""


if __name__ == "__main__":
    say("Hello Tharun, I am your Jarvis AI.")

    while True:
        print("Listening...")
        query = takeCommand()
        if not query:
            continue

        if query.strip() in ["stop", "exit", "quit"]:
            say("Okay, stopping boss.")
            break

       
        if "using artificial intelligence" in query:
            ai(query)
            continue

        
        sites = {
            "youtube": "https://www.youtube.com",
            "wikipedia": "https://www.wikipedia.com",
            "instagram": "https://www.instagram.com",
            "google": "https://www.google.com"
        }

        for name, url in sites.items():
            if f"open {name}" in query:
                say(f"Opening {name} boss")
                webbrowser.open(url)

        
        if "time" in query:
            now = datetime.datetime.now().strftime("%H:%M")
            say(f"The time is {now} boss")

        