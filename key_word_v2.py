import speech_recognition as sr

r = sr.Recognizer()



while(True):
    with sr.Microphone(device_index=10) as source:
        
        print("Escuchando...")
        r.adjust_for_ambient_noise(source)
        data = r.listen(source)
        
        text = r.recognize_google(data, language='es-ES')

        if "hola" in text.split(' '):
            print("Hola detectado ... \n")
            break
        else:
            print(".....")



print("Di tu frase.. ")

with sr.Microphone(device_index=10) as source:
    try:
        data = r.record(source, duration=5)
        text = r.recognize_google(data, language='es-ES')
        print(text)
    except:
        print("Nada detectado")





