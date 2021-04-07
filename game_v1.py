import enum



class gameState(enum.Enum):
    inicial = 0
    saludo = 1
    espera_saludo = 2
    explicacion_regla_juego = 3
    espera_confirmacion_regla_juego = 4
    juego = 5
    fin_juego = 6

estado_actual = gameState.inicial

def personaPresente():
    return True

while(True):

    if estado_actual == gameState.inicial:
        print("inicio")
        estado_actual = gameState.saludo
    elif estado_actual == gameState.saludo:
        print("un saludo")
        estado_actual = gameState.espera_saludo
    elif estado_actual == gameState.espera_saludo:
        print("espera saludo")
        if not personaPresente():
            estado_actual = gameState.saludo
        else:
            estado_actual = gameState.explicacion_regla_juego
    elif estado_actual == gameState.explicacion_regla_juego:
        print("Explica juego")
        estado_actual = gameState.espera_confirmacion_regla_juego
    elif estado_actual == gameState.espera_confirmacion_regla_juego:
        print("esperando confinrmacion regla_juego")
        estado_actual = gameState.juego
    elif estado_actual == gameState.juego and not personaPresente():
        print("suspenderJuego()")
        estado_actual = gameState.inicial
    elif estado_actual == gameState.juego:
        print("juego()")
        estado_actual = gameState.fin_juego
    elif estado_actual == gameState.fin_juego:
        print("WIN!")
        #fin()
        estado_actual = gameState.inicial
        exit()



