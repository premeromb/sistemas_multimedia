# import the opencv library
import cv2
from dt_apriltags import Detector
import numpy as np
import time
import enum

import dlib

import operator


import struct
import pyaudio
import pvporcupine

import face_recognition
import eyes_recognition

from gtts import gTTS

from time import sleep

import os
import pyglet


from playsound import playsound

at_detector = Detector(families='tag16h5',
                       nthreads=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)

camera_params = (336.7755634193813, 336.02729840829176,
                 333.3575643300718, 212.77376312080065)

capture_duration = 4



# define a video capture object
vid = cv2.VideoCapture(0)

# Check if camera opened successfully
if (vid.isOpened() == False):
  print("Error opening video  file")


class gameState(enum.Enum):
    inicial = 0
    saludo = 1
    espera_saludo = 2
    explicacion_regla_juego = 3
    espera_confirmacion_regla_juego = 4
    juego = 5
    fin_juego = 6

estado_actual = gameState.inicial

def speak (text):
    tts = gTTS(text=text, lang='es')
    filename = 'temp.mp3'
    tts.save(filename)
    playsound(filename)
    os.remove(filename) #remove temperory file

def saludo():
    speak("¡Hola! me llamo terminator")

def mensajeFinJuego():
     speak("¡Enhorabuena, has ganado!")

def mensajeCambioPosiociones(ficha1, ficha2):
    speak("Cambia la posición {} por la {}".format(ficha1, ficha2))

def explicaJuego():
    speak("mensaje")
    #speak(text='En esta primera versión, pondremos en orden creciente las fichas intercambiando sus posiciones.')




def esperaSaludo(): # añadir un temporizador que dado un tiempo maximo se salga con resultado de error
    print("entra en esperaSaludo")

    porcupine = None
    pa = None
    audio_stream = None

    try:
        porcupine = pvporcupine.create(keywords=['terminator'], sensitivities=[1.0])

        pa = pyaudio.PyAudio()

        audio_stream = pa.open(
                        rate=porcupine.sample_rate,
                        channels=1,
                        format=pyaudio.paInt16,
                        input=True,
                        frames_per_buffer=porcupine.frame_length,
                        input_device_index=11)

        print("Microfono listo")
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("DETECTADA!")
                # pa.close()
                break
        
    finally:
        if porcupine is not None:
            porcupine.delete()

        if audio_stream is not None:
            audio_stream.close()

        if pa is not None:
                pa.terminate()
                
    print("sale de esperaSaludo")



def buscaCaras():
    #return face_recognition.recognition()
    return eyes_recognition.detector()

def checkForTags():

  start_time = time.time()

  captured = []

  while int(time.time() - start_time) < capture_duration:

      # Capture the video frame
      # by frame
      ret, frame = vid.read()
      grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

      # Display the resulting frame
      cv2.imshow('frame', grayFrame)

      tags = at_detector.detect(grayFrame, True, camera_params, 0.2)

      tag_ids = [tag.tag_id for tag in tags]

      #if len(tag_ids) > 0:
      #  print(tag_ids)

      color_img = cv2.cvtColor(grayFrame, cv2.COLOR_GRAY2RGB)

      for tag in tags:
          if tag.decision_margin > 65:

              for idx in range(len(tag.corners)):
                  cv2.line(color_img, tuple(
                      tag.corners[idx-1, :].astype(int)), tuple(tag.corners[idx, :].astype(int)), (0, 255, 0))

                  cv2.putText(color_img, str(tag.tag_id),
                              org=(tag.corners[0, 0].astype(
                                  int)+10, tag.corners[0, 1].astype(int)+10),
                              fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                              fontScale=0.8,
                              color=(0, 0, 255))

              if tag.tag_id not in [tag.tag_id for tag in captured]:
                captured.append(tag)

      cv2.imshow('Detected tags for ', color_img)

      # the 'q' button is set as the
      # quitting button you may use any
      # desired button of your choice
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break

  return captured


def getTagsIdOrder():

    print("\n    .... BUSCANDO TAGS .... \n")

    tagsOnTable = checkForTags()

    tagsOnTable.sort(key=lambda x: x.center[0], reverse=True)

    return [tag.tag_id for tag in tagsOnTable]


def waitForAcction():
    print("Waiting ....")
    time.sleep(3)
    print("Time is up!")

def juego ():

    #print ("La accion elegida ha sido {}".format(accion))
    print("\nOrdena la secuencia\n")

    secuencia = getTagsIdOrder()


    while (True):

        print("\n  Estado actual {}".format(secuencia))

        if secuencia == [0, 1, 6]:
            print("No hay que hacer nada: WIN!")
            estado_actual == gameState.fin_juego
            break
        elif secuencia == [0, 6, 1]:
            print("   ACCION: Cambio de posicion 2/3")
            mensajeCambioPosiociones(2,3)
            waitForAcction()
            secuencia = getTagsIdOrder()
        elif secuencia == [1, 0, 6]:
            print("   ACCION: Cambio de posicion 1/2")
            mensajeCambioPosiociones(1,2)
            waitForAcction()
            secuencia = getTagsIdOrder()
        elif secuencia == [1, 6, 0]:
            print("   ACCION: Cambio de posicion 1/2")
            mensajeCambioPosiociones(1,2)
            waitForAcction()
            secuencia = getTagsIdOrder()
        elif secuencia == [6, 0, 1]:
            print("   ACCION: Cambio de posicion 1/2")
            mensajeCambioPosiociones(1,2)
            waitForAcction()
            secuencia = getTagsIdOrder()
        elif secuencia == [6, 1, 0]:
            print("   ACCION: Cambio de posicion 3/1")
            mensajeCambioPosiociones(3,1)
            waitForAcction()
            secuencia = getTagsIdOrder()
        else: 
            print("ERROR: Secuencia detectada invalida")
            secuencia = getTagsIdOrder()
            

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


def personaPresente():
    return face_recognition.recognition()


def logicaJuego():

    global estado_actual

    while(True):

        if estado_actual == gameState.inicial:
            print("inicio")
            estado_actual = gameState.saludo
        elif estado_actual == gameState.saludo:
            print("un saludo")
            saludo()
            estado_actual = gameState.espera_saludo
            print("    ¿Hay alguien ahi?")
            if not personaPresente():
                print("    no hay nadie presente")
                estado_actual = gameState.saludo
            else:
                print("    detecta persona")
                estado_actual = gameState.espera_saludo
        elif estado_actual == gameState.espera_saludo:
            print("espera saludo")
            esperaSaludo()
            estado_actual = gameState.explicacion_regla_juego             
        elif estado_actual == gameState.explicacion_regla_juego:
            print("Explica juego")
            estado_actual = gameState.espera_confirmacion_regla_juego
            explicaJuego()
            # print("    ¿Hay alguien ahi?")
            # if not personaPresente():
            #     print("    no hay nadie presente")
            #     estado_actual = gameState.saludo
            # else:
            #     print("    detecta persona")
            #     estado_actual = gameState.espera_confirmacion_regla_juego
        elif estado_actual == gameState.espera_confirmacion_regla_juego:
            print("esperando confinrmacion regla_juego")
            estado_actual = gameState.juego
            esperaSaludo()
        elif estado_actual == gameState.juego:
            print("juego()")
            estado_actual = gameState.fin_juego
            juego()
        elif estado_actual == gameState.fin_juego:
            print("WIN!")
            estado_actual = gameState.inicial
            mensajeFinJuego()
            exit()

logicaJuego()
