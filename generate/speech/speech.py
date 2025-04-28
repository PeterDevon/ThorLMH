
import speech_recognition as sr
import pyttsx3
from ollama import chat, ChatResponse

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)

# Words to completely remove from the recognized text
BANNED_WORDS = [
    "asterisk", "percent", "comma", "period", 
    "question", "mark", "exclamation", "point", 
    "colon", "semicolon", "dash", "hyphen", 
    "underscore", "slash", "backslash", 
    "equals", "plus"
]

def speak(text):
    """Speak out the given text using pyttsx3."""
    tts_engine.say(text)
    tts_engine.runAndWait()

def clean_text(text):
    """Remove unwanted words like 'asterisk', 'comma', etc. from the text."""
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in BANNED_WORDS]
    return ' '.join(filtered_words)

def listen_once_and_return(output_box, attached_image=None):
    from ollama import chat
    import speech_recognition as sr
    import pyttsx3

    recognizer = sr.Recognizer()
    tts_engine = pyttsx3.init()
    tts_engine.setProperty('rate', 150)

    def speak(text):
        tts_engine.say(text)
        tts_engine.runAndWait()

    with sr.Microphone() as source:
        try:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            recognizer.energy_threshold = 300
            recognizer.dynamic_energy_threshold = True
            recognizer.pause_threshold = 1.2

            output_box.configure(state="normal")
            output_box.insert("end", "Ready to listen. Speak now!\n")
            output_box.update_idletasks()

            audio = recognizer.listen(source, timeout=None)
            raw_text = recognizer.recognize_google(audio)
            output_box.insert("end", f"You said: {raw_text}\nThor: ")
            output_box.update_idletasks()

            # FIX: Always use the correct model name
            messages = [{'role': 'user', 'content': raw_text}]
            if attached_image:
                messages.append({'role': 'user', 'images': [attached_image]})

            stream = chat(model='gemma3:4b', messages=messages, stream=True)
            full_response = ""

            for chunk in stream:
                token = chunk['message']['content']
                output_box.insert("end", token)
                output_box.update_idletasks()
                full_response += token

            speak(full_response)
            output_box.insert("end", "\n")
            output_box.configure(state="disabled")

        except sr.WaitTimeoutError:
            output_box.insert("end", "No speech detected (timeout).\n")
        except sr.UnknownValueError:
            output_box.insert("end", "Could not understand audio.\n")
        except sr.RequestError as e:
            output_box.insert("end", f"Google Speech Recognition service error: {e}\n")

