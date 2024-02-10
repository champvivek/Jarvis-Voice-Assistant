import pyttsx3
import requests
import speech_recognition as sr
import datetime
import os
import cv2
import random
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import sys
import time
import pyjokes
import pyautogui
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from jarvisUI import Ui_MainWindow
import operator
from bs4 import BeautifulSoup
from pywikihow import search_wikihow
import psutil
import speedtest

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# Text to Speech Code
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


# To Wish
def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")

    if hour >= 3 and hour < 12:
        speak(f"Good Morning, its {tt}")
    elif hour >= 12 and hour < 18:
        speak(f"Good Afternoon, its {tt}")
    else:
        speak(f"Good Evening, its {tt}")
    speak("I am Jarvis sir, Please tell me how can I help you")


class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    # To Convert Voice into Text
    def takecommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source, timeout=7, phrase_time_limit=5)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"user said: {query}")

        except Exception as e:
            speak("Say that again please...")
            return "none"
        return query

    def TaskExecution(self):
        wish()
        while True:

            self.query = self.takecommand().lower()

            # Logic building for Tasks

            if "open notepad" in self.query:
                npath = "C:\\Windows\\System32\\notepad.exe"
                os.startfile(npath)

            elif "open adobe reader" in self.query:
                apath = "C:\\Program Files\\Adobe\\Acrobat DC\\Acrobat\\Acrobat.exe"
                os.startfile(apath)

            elif "open command prompt" in self.query:
                os.system("start cmd")

            elif "open camera" in self.query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    k = cv2.waitKey(50)
                    if k == 27:
                        break;
                cap.release()
                cv2.destroyAllWindows()

            elif "play music" in self.query:
                music_dir = "D:\\Coding\\Python Project\\Songs"
                songs = os.listdir(music_dir)
                rd = random.choice(songs)
                os.startfile(os.path.join(music_dir, rd))

            elif "ip address" in self.query:
                ip = get('https://api.ipify.org').text
                speak(f"Your IP Address is {ip}")


            elif "wikipedia" in self.query:

                try:

                    speak("Searching Wikipedia...")

                    query = self.query.replace("wikipedia", "")

                    results = wikipedia.summary(query, sentences=2)

                    speak("According to Wikipedia")

                    speak(results)

                except Exception as e:

                    print(f"An error occurred during Wikipedia search: {e}")


            elif "open youtube" in self.query:
                webbrowser.open("www.youtube.com")

            elif "open linkedin" in self.query:
                webbrowser.open("www.linkedin.com")

            elif "open hotstar" in self.query:
                webbrowser.open("www.hotstar.com")

            elif "open netflix" in self.query:
                webbrowser.open("www.netflix.com")

            elif "open prime video" in self.query:
                webbrowser.open("www.primevideo.com")

            elif "open jiocinema" in self.query:
                webbrowser.open("www.jiocinema.com")

            elif "open zee5" in self.query:
                webbrowser.open("www.zee5.com")

            elif "open google" in self.query:
                speak("Sir, What should I search on google")
                cm = self.takecommand().lower()
                webbrowser.open(f"{cm}")

            elif "play song on youtube" in self.query:
                speak("Sir, What should I play on youtube")
                ym = self.takecommand().lower()
                kit.playonyt(f"{ym}")

            elif "no thanks" in self.query:
                speak("Thanks for using me, Have a good day")
                sys.exit()

            # speak("sir, do you have any other work")

            # To close any application
            elif "close notepad" in self.query:
                speak("okay sir, closing notepad")
                os.system("taskkill /f /im notepad.exe")

            # To find a joke
            elif "tell me a joke" in self.query:
                joke = pyjokes.get_joke()
                speak(joke)

            elif "shut down the system" in self.query:
                os.system("shutdown /s /t 5")

            elif "restart the system" in self.query:
                os.system("shutdown /r /t 5")

            elif "sleep the system" in self.query:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

            elif "switch the window" in self.query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

            elif "where i am" in self.query or "where we are" in self.query:
                speak("Wait sir, let me check")
                try:
                    ipAdd = requests.get('https://api.ipify.org').text
                    print(ipAdd)
                    url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
                    geo_requests = requests.get(url)
                    geo_data = geo_requests.json()
                    city = geo_data['city']
                    country = geo_data['country']
                    speak(f"Sir I am not sure, but I think we are in {city} city of {country} country")
                except Exception as e:
                    speak("Sorry sir, Due to network issue I am not able to find where I am")
                    pass

            elif "take a screenshot" in self.query:
                speak("Sir, please tell me the name for this screenshot file")
                name = self.takecommand().lower()
                speak("Please sir hold the screen for few seconds, I am taking screenshot")
                time.sleep(3)
                img = pyautogui.screenshot()
                img.save(f"{name}.png")
                speak("I am done sir, the screenshot is saved in our main folder, now I am ready for the next command")

            elif "hide all files" in self.query or "hide this folder" in self.query or "visible for everyone" in self.query:
                speak("sir please tell me you want to hide this folder or make it visible for everyone")
                condition = self.takecommand().lower()
                if "hide" in condition:
                    os.system("attrib +h /s /d")
                    speak("Sir, all the files in this folder are now hidden.")

                elif "visible" in condition:
                    os.system("attrib -h /s /d")
                    speak("sir, all the files in this folder are now visible to everyone.")

                elif "leave it" in condition or "leave for now" in condition:
                    speak("Ok sir")

            elif "can you calculate" in self.query:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    speak("Say what you want to calculate, for example 3 plus 5")
                    print("listening...")
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                my_string = r.recognize_google(audio)
                print(my_string)

                def get_operator_fn(op):
                    return {
                        '+': operator.add,
                        '-': operator.sub,
                        'x': operator.mul,
                        'divided': operator.__truediv__,
                    }[op]

                def eval_binary_expr(op1, oper, op2):
                    op1, op2 = int(op1), int(op2)
                    return get_operator_fn(oper)(op1, op2)

                speak("Your result is")
                speak(eval_binary_expr(*(my_string.split())))

            elif "hello" in self.query or "hey" in self.query:
                speak("hello sir, May I help you with something")

            elif "how are you" in self.query or "how r u" in self.query:
                speak("I am fine sir, what about you")

            elif "also good" in self.query or "fine" in self.query:
                speak("That's great to hear from you")

            elif "thank you" in self.query or "thanks" in self.query:
                speak("it's my pleasure sir")

            elif "you can sleep" in self.query or "sleep now" in self.query:
                speak("okay sir, I am going to sleep now you can call me anytime")
                sys.exit()

            elif "temperature" in self.query:
                speak("Please tell me the city")
                search = self.takecommand().lower()
                url = f"https://www.google.com/search?q=temperature+in+{search}"
                r = requests.get(url)
                data = BeautifulSoup(r.text, "html.parser")
                temp = data.find("div", class_="BNeawe").text
                speak(f"Current Temperature of {search} is {temp}")

            elif "activate how to do mode" in self.query:
                speak("How to do mode is activated please tell me what you want to know")
                how = self.takecommand()
                max_results = 1
                how_to = search_wikihow(how, max_results)
                assert len(how_to) == 1
                how_to[0].print()
                speak(how_to[0].summary)

            elif "how much power we have" in self.query or "how much power left" in self.query or "battery" in self.query:
                battery = psutil.sensors_battery()
                percentage = battery.percent
                speak(f"Sir, our system have {percentage} percent battery left")
                if percentage >= 75:
                    speak("We have enough power to continue our work")
                elif percentage >= 40 and percentage < 75:
                    speak("We should connect our system to charging point to charge our battery")
                elif percentage >= 15 and percentage < 40:
                    speak("We don't have enough power to work, please connect to charging point")
                elif percentage > 0 and percentage < 15:
                    speak("We have very low power, system will shut down soon")

            elif "internet speed" in self.query:
                st = speedtest.Speedtest()
                dl = st.download()
                up = st.upload()
                speak(f"sir we have {dl} bit per second downloading speed and {up} bit per second uploading speed")

            elif "volume up" in self.query:
                pyautogui.press("volumeup")

            elif "volume down" in self.query:
                pyautogui.press("volumedown")

            elif "volume mute" in self.query or "mute" in self.query:
                pyautogui.press("volumemute")




startExecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Start.clicked.connect(self.startTask)
        self.ui.Start_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("C:/Users/vivek/OneDrive/Desktop/connections.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)


app = QApplication(sys.argv)
Jarvis = Main()
Jarvis.show()
exit(app.exec_())
