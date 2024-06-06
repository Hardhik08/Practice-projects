import tkinter  
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import cv2
import random
import re
import requests
from bs4 import BeautifulSoup

print('Loading your AI personal assistant - Pink AI')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_user():
    current_time = datetime.datetime.now().strftime("%H")
    if 0 <= int(current_time) < 12:
        speak("Good morning! I am Pink AI, your personal assistant. I can assist you with various tasks. How can I help you?")
    elif 12 <= int(current_time) < 18:
        speak("Good afternoon! I am Pink AI, your personal assistant. I can assist you with various tasks. How can I help you?")
    else:
        speak("Good evening! I am Pink AI, your personal assistant. I can assist you with various tasks. How can I help you?")

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            statement = recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {statement}\n")
        except Exception as e:
            speak("Sorry, I didn't catch that. Can you repeat?")
            return "None"
        return statement

speak("Loading your AI personal assistant Pink AI")
greet_user()

def extract_time(input_text):
    # Regular expression pattern to match time in HH:MM AM/PM format
    pattern = r'(\d{1,2}):(\d{2})\s+(AM|PM)'
    match = re.search(pattern, input_text, re.IGNORECASE)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2))
        meridian = match.group(3).upper()
        
        # Convert 12-hour format to 24-hour format
        if hour == 12:
            hour = 0
        if meridian == 'PM':
            hour += 12

        # Return the time in HH:MM format
        return f"{hour:02d}:{minute:02d}"
    else:
        return None

def set_reminder(reminder_text, reminder_time):
    try:
        # Parse the time string
        reminder_time_obj = datetime.datetime.strptime(reminder_time, "%I:%M %p")
        reminder_time = reminder_time_obj.strftime("%H:%M")  # Convert to HH:MM format
        current_time = datetime.datetime.now().strftime("%H:%M")

        # Check if the reminder time is in the past
        if reminder_time_obj < datetime.datetime.now():
            speak("Sorry, I can't set a reminder for a past time.")
            return

        # Acknowledge the reminder
        speak(f"Reminder set for {reminder_time_obj.strftime('%I:%M %p')} - {reminder_text}")

        # Calculate the time difference until the reminder
        time_difference = (reminder_time_obj - datetime.datetime.now()).total_seconds()

        # Sleep until the reminder time
        time.sleep(time_difference)

        # Notify about the reminder
        speak(f"Reminder: {reminder_text}")
            
    except ValueError:
        speak("Sorry, I couldn't understand the time format. Please provide the time in HH:MM AM/PM format.")

def capture_image():
    speak("Initializing camera. Please look at the camera and smile!")
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        speak("Error: Unable to access the camera.")
        return

    # Capture frame-by-frame
    ret, frame = cap.read()

    # Save the captured frame to a file
    if ret:
        cv2.imwrite("captured_image.jpg", frame)
        speak("Photo captured successfully!")
    else:
        speak("Error: Failed to capture the photo.")

    # Release the camera
    cap.release()

def handle_commands():
    while True:
        speak("How can I assist you?")
        statement = listen_command().lower()

        if statement == "none":
            continue

        if 'set a reminder' in statement:
            speak("What should I remind you about?")
            reminder_text = listen_command()
            
            # Extract time from user input
            speak("When should I remind you? Please provide the time in HH:MM AM/PM format, for example, 1:35 PM.")
            time_input = listen_command()
            reminder_time = extract_time(time_input)
            
            if reminder_time:
                # Set the reminder
                set_reminder(reminder_text, reminder_time)
            else:
                speak("Sorry, I couldn't understand the time format. Please try again.")
        
        elif 'take a photo' in statement or 'capturing an image of mine' in statement or 'click a photo' in statement:
            capture_image()

        elif 'time' in statement:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}")

        elif 'news' in statement:
            speak("Here are some headlines from the Times of India:")
            url = "https://timesofindia.indiatimes.com/home/headlines"
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                headlines = soup.find_all('span', class_='w_tle')
                for i, headline in enumerate(headlines[:5]):
                    speak(f"Headline {i+1}: {headline.text.strip()}")
                    time.sleep(2)  # Pause between each headline

        elif 'joke' in statement:
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Parallel lines have so much in common. It's a shame they'll never meet.",
                "I told my wife she was drawing her eyebrows too high. She looked surprised.",
                "Why did the scarecrow win an award? Because he was outstanding in his field!",
                "I'm reading a book on anti-gravity. It's impossible to put down!"
            ]
            joke = random.choice(jokes)
            speak(joke)
            speak("Ha ha ha ha!")

        elif 'youtube' in statement:
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")

        elif 'wikipedia' in statement:
            speak("What do you want to search on Wikipedia?")
            search_query = listen_command().lower()
            try:
                result = wikipedia.summary(search_query, sentences=2)
                speak("According to Wikipedia:")
                speak(result)
            except wikipedia.exceptions.PageError:
                speak("Sorry, I couldn't find any information on that topic.")
            except wikipedia.exceptions.DisambiguationError:
                speak("There are multiple matches for that query. Please be more specific.")

        elif 'exit' in statement or 'quit' in statement:
            speak("Exiting Pink AI. Goodbye!")
            break

        else:
            speak("Sorry, I didn't understand that. Can you please repeat?")

handle_commands()
