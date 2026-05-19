import matplotlib.pyplot as plt
import numpy as np

from scripts.leer_datos import leer_datos
from scripts.procesar_senal import procesar_senal
from scripts.fft_espectral import fft_espectral

def comparar():

    #Aquí se pondran la ruta de los archivos de la arpeta datos
    archivos = {
        "Caminar": "datos/caminar.csv", 
        "Correr": "datos/correr.csv"
        }

    datos = {} #guardara las señales procesadas y sus resultados espectrales

    for actividad, archivo in archivos.items():

        t, ax, ay, az = leer_datos(archivo) #Lectura del CSV y separación de columnas del acelerómetro

        senal = procesar_senal(ax, ay, az) #Cálculo de magnitud y eliminación de componente DC

        (f, P1, frecuencia_dom, cadencia, pico_max, energia_espectral, f_psd, psd) = fft_espectral(senal, t) #Análisis espectral: FFT, PSD y métricas principales


        datos[actividad] = {
            "t": t, 
            "senal": senal, 
            "f": f, 
            "P1": P1, 
            "f_psd": f_psd, 
            "psd": psd, 
            "freq": frecuencia_dom, 
            "cad": cadencia, 
            "pico": pico_max, 
            "energia": energia_espectral
            }

    fig, axes = plt.subplots(3, 1, figsize=(12,10)) #Figura comparativa: tiempo, FFT y PSD

    fig.suptitle("Comparación: Caminar vs Correr", fontsize=18, fontweight="bold")

    #Comparación en el dominio del tiempo
    for actividad in datos:
        axes[0].plot(datos[actividad]["t"], datos[actividad]["senal"], label=actividad)

    axes[0].set_title("Señal Temporal")
    
    axes[0].set_xlabel("Tiempo (s)")

    axes[0].set_ylabel("Magnitud")

    axes[0].grid(True)
    axes[0].legend()

    #Comparación en el dominio de la frecuencia mediante FFT
    for actividad in datos:
        axes[1].plot(datos[actividad]["f"], datos[actividad]["P1"], label=actividad)

    axes[1].set_xlim(0,10)

    axes[1].set_title("Análisis Espectral FFT")

    axes[1].set_xlabel("Frecuencia (Hz)")

    axes[1].set_ylabel("Magnitud")

    axes[1].grid(True)
    axes[1].legend()

    #Comparación de potencia espectral mediante PSD
    for actividad in datos:
        axes[2].semilogy(datos[actividad]["f_psd"], datos[actividad]["psd"], label=actividad)

    axes[2].set_xlim(0,10)

    axes[2].set_title("Densidad Espectral de Potencia")

    axes[2].set_xlabel("Frecuencia (Hz)")

    axes[2].set_ylabel("Potencia")

    axes[2].grid(True)
    axes[2].legend()

    plt.tight_layout(rect=[0,0,1,0.97])
    plt.savefig("resultados/comparacion_caminar_correr.png", dpi=300, bbox_inches="tight")
    plt.show()