import requests
import json


def speak(str):
    import pyttsx3
    converter = pyttsx3.init()
    voices = converter.getProperty('voices')
    converter.setProperty('voice', voices[0].id)
    converter.setProperty('rate', 250)
    converter.setProperty('volume', 125)
    converter.say(str)
    converter.runAndWait()

if __name__ == '__main__':
    r = requests.get("https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=796ab5394b5d42fdabf274a6b54fe027")
    data = r.text
    parsed = json.loads(data)    
    
    name = 'Aryan Jhaveri'
    speak(f'Hello, {name}. Here are the top 5 headlines in the United States today...')
    
    for i in range(0, 5):
        speak(f"{i + 1}")
        speak(parsed['articles'][i]['title'])
        i += 1

# good voices : 0M, 7M, 10F, 17F, 