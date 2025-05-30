import speech_recognition as sr

class Voice_Recognition:
    def __init__(self):
        self.text = ""

    def get_voice_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something! \n\n")
            audio = recognizer.listen(source)
        try:
            self.text = recognizer.recognize_sphinx(audio)
            return str(self.text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio. ❌")
            self.get_voice_input()
        except sr.RequestError as e:
            print(f"Could not request results: {e}. ❌")
            self.get_voice_input()