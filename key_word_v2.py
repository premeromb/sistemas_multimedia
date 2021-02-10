import speech_recognition as sr

r = sr.Recognizer()

while(True):
    with sr.Microphone() as source:
        print("Grabando...")
        r.adjust_for_ambient_noise(source)
        data = r.record(source, duration=3)
        
        text = r.recognize_google(data,language='es')
        print("Fin....")
        if "hola" in text.split(' '):
            break

print(text)