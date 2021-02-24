#!/usr/bin/env python3
import struct
import pyaudio
import pvporcupine
import speech_recognition as sr

r = sr.Recognizer()

porcupine = None
pa = None
audio_stream = None


def recognition_phrase():
    print("Di tu frase.. ")
    audio_stream.close()
    with sr.Microphone(device_index=10) as source:
        try:
            data = r.record(source, duration=5)
            text = r.recognize_google(data, language='es-ES')
            print(text)
        except:
            print("Nada detectado")


try:
    porcupine = pvporcupine.create(keywords=['terminator'], sensitivities=[1.0])

    pa = pyaudio.PyAudio()

    audio_stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length,
                    input_device_index=10)

    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            print("DETECTADA!")
            break
            
except:
    if porcupine is not None:
        porcupine.delete()

    if audio_stream is not None:
        audio_stream.close()

    if pa is not None:
        pa.terminate()


recognition_phrase()