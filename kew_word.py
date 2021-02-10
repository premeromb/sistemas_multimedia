import speech_recognition as sr

r = sr.Recognizer()

file = sr.AudioFile("output.wav")

print("eeee")

while(True):
    with file as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)
        result = r.recognize_google(audio,language='es')
    if "hola" in result.split(' '):
        break

print("Done!")

print(result)