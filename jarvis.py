import datetime
from numpy import take
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import asyncio
import python_weather 
import random


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[1].id)
engine.setProperty('voice',voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    
    speak("I am Jarvis Sir. Please tell me how may I help you")

def takeCommand():
    #It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('dipurawat1999@gmail.com','your-password')
    server.sendmail('dipurawat1999@gmail.com',to,content)
    server.close()

async def getweather():
    # declare the client. format defaults to metric system (celcius, km/h, etc.)
    client = python_weather.Client(format=python_weather.IMPERIAL)

    # fetch a weather forecast from a city
    weather = await client.find("Delhi")

    # returns the current day's forecast temperature (int)
    print(weather.current.temperature)

    # get the weather forecast for a few days
    for forecast in weather.forecasts:
        print(str(forecast.date), forecast.sky_text, forecast.temperature)

    # close the wrapper once done
    await client.close()


if __name__ =="__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
    #logic for executing tasks based on query'
        if 'wikipedia' in query:
            speak("Searching wikipedia...")
            query  = query.replace("wikipedia","")
            results = wikipedia.summary(query,sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")
        elif 'open github' in query:
            webbrowser.open("github.com")

        elif 'play music' in query:
            n = random.randint(0,7)
            music_dir = 'G:\\music'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir,songs[n]))

        elif 'the time' in query:
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strtime}")
        
        elif 'open code' in query:
            codePath = "C:\\Users\\Acer\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
        
        elif 'email to deepak' in query:
            try:
                 speak("What should I say?")
                 content = takeCommand()
                 to = "akkudeepu2027@gmail.com"
                 sendEmail(to, content)
                 speak("Email has been sent!")
            except Exception as e:
                #print(e)
                speak("Sorry my friend Deepak bhai.I am not able to send this mail")
        
        elif 'the weather' in query:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(getweather())
            speak(f"Today's weather is {loop}")

        elif 'quit jarvis' in query:
            speak("Thank you for using our services. Have a nice day!!")
            exit()





