import speech_recognition as sr
from gtts import gTTS
import pyjokes
import wikipedia as wkp
from datetime import datetime
from ecapture import ecapture as ec
import webbrowser as bro
import openai
import os
import playsound

username = None

def listen():
    input = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = input.listen(source)
        try:
            data = input.recognize_google(audio)
            print("You said: " + data)
        except sr.UnknownValueError:
            print("Sorry, I didn't get that. Please try again!")
            data = listen()
    return data

def respond(output):
    response = gTTS(text=output, lang="en", slow=False)
    response.save("response.mp3")
    playsound.playsound("response.mp3", True)
    os.remove("response.mp3")

while (True):
    data = input("Enter your command: ")
    data.lower()
    if "bye" in data or "stop" in data or "exit" in data:
        respond("Okay, bye. Take care.")
        exit()
    elif "time" in data or "date" in data:
        response = ''
        if "time" in data and "date" in data:
            response = "The time is " + datetime.now().strftime("%H:%M") + " and the date is " + datetime.now().strftime("%d/%m/%Y")
        elif "time" in data:
            response = "The time is " + datetime.now().strftime("%H:%M")
        elif "date" in data:
            response = "The date is " + datetime.now().strftime("%d/%m/%Y")
        respond(response)
        
    elif "search for" in data:
        dataIndex = data.split().index("for")
        topic = " ".join(data.split()[dataIndex+1:])
        respond("Okay, searching for " + topic)
        bro.open("https://www.google.com/search?q=" + topic)
    elif "joke" in data:
        respond("Okay, here is a joke.")
        respond(pyjokes.get_joke())
    elif "repeat" in data:
        data = data.split()
        respond(" ".join(data[data.index("repeat")+1:]))
    elif "who" in data:
        if data == "who are you":
            respond("I am your assistant, Alice. I can help you out with basic tasks. To know what I can do, press * on your keyboard.")
            choice = input()
        elif data == "who am i":
            if username is not None:
                respond("You are " + username + ", or at least that is what you told me.")
            else:
                respond("You have not told me your name. Kindly type it.")
                username = input("Enter the name here: ")
        elif "who is" in data:
            name = " ".join(data.split()[2:])
            who_is = wkp.summary(wkp.search(name)[0]).split(".")
            size = min(3, len(who_is))
            response = ''
            for i in range(size):
                response += who_is[i]
            respond("Here is what I received from Wikipedia: " + response)
    else:
        # get api key from environment variable
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.Completion.create(
            model             = "text-davinci-002",
            prompt            = data,
            temperature       =   0.9,
            max_tokens        = 1000,
            stop              =["?"]
        )
        print(response['choices'][0]['text'])
        respond(response['choices'][0]['text'])