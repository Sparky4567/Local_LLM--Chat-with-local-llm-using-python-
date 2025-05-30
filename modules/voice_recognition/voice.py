import speech_recognition as sr

class Voice_Recognition:
    def __init__(self):
        self.text = ""

    def get_voice_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!\n\n")
            audio = recognizer.listen(source)
        try:
            print("You said: " + recognizer.recognize_sphinx(audio))
        except sr.UnknownValueError:
            print("Could not understand audio. Try again. \n\n")
            self.get_voice_input()
        except sr.RequestError as e:
            print(f"Sphinx error: {e}\n\n")
            self.get_voice_input()
        except Exception as e:
            print(f"Error: {e}")
            self.get_voice_input()