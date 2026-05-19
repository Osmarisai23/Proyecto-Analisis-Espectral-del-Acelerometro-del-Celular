import numpy as np

def procesar_senal(ax, ay, az):

    magnitud = np.sqrt(ax**2 + ay**2 + az**2) #Cálculo de la magnitud vectorial del acelerómetro

    magnitud_ac = magnitud - np.mean(magnitud) #Eliminación de la componente DC

    return magnitud_ac