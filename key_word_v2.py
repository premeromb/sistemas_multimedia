import speech_recognition as sr

r = sr.Recognizer()

print("Grabando...")

while(True):
    with sr.Microphone(device_index=10) as source:

        r.adjust_for_ambient_noise(source)
        data = r.listen(source)
        
        text = r.recognize_google(data,language='es')

        if "hola" in text.split(' '):
            break
        else:
            print("No hola..")

print("Fin....")

print(text)

