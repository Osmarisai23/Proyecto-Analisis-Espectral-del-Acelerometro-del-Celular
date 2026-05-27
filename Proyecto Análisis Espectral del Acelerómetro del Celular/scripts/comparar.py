import numpy as np
from scripts.leer_datos import leer_datos
from scripts.procesar_senal import procesar_senal
from scripts.fft_espectral import fft_espectral

def comparar(ruta_caminar, ruta_correr, fig, axes):
    # Mapeamos las rutas dinámicas enviadas por la interfaz
    archivos = {
        "Caminar": ruta_caminar, 
        "Correr": ruta_correr
    }

    datos = {} 

    for actividad, archivo in archivos.items():
        t, ax, ay, az = leer_datos(archivo)
        senal = procesar_senal(ax, ay, az)
        (f, P1, frecuencia_dom, cadencia, pico_max, energia_espectral, f_psd, psd) = fft_espectral(senal, t)

        datos[actividad] = {
            "t": t, "senal": senal, "f": f, "P1": P1, "f_psd": f_psd, "psd": psd
        }

    # Limpiamos los ejes previos antes de dibujar de nuevo
    for ax in axes:
        ax.clear()

    fig.suptitle("Comparación Simultánea: Caminar vs Correr", fontsize=14, fontweight="bold", color="#cdd6f4")

    # 1. Señal Temporal
    for actividad in datos:
        axes[0].plot(datos[actividad]["t"], datos[actividad]["senal"], label=actividad)
    axes[0].set_title("Señal Temporal", color="#cba6f7", fontsize=10)
    axes[0].set_xlabel("Tiempo (s)", color="#cdd6f4")
    axes[0].set_ylabel("Magnitud", color="#cdd6f4")
    axes[0].grid(True, linestyle="--", alpha=0.5)
    axes[0].legend()

    # 2. Análisis Espectral FFT
    for actividad in datos:
        axes[1].plot(datos[actividad]["f"], datos[actividad]["P1"], label=actividad)
    axes[1].set_xlim(0, 10)
    axes[1].set_title("Análisis Espectral FFT", color="#cba6f7", fontsize=10)
    axes[1].set_xlabel("Frecuencia (Hz)", color="#cdd6f4")
    axes[1].set_ylabel("Magnitud", color="#cdd6f4")
    axes[1].grid(True, linestyle="--", alpha=0.5)
    axes[1].legend()

    # 3. Densidad Espectral de Potencia (PSD)
    for actividad in datos:
        axes[2].semilogy(datos[actividad]["f_psd"], datos[actividad]["psd"], label=actividad)
    axes[2].set_xlim(0, 10)
    axes[2].set_title("Densidad Espectral de Potencia (PSD)", color="#cba6f7", fontsize=10)
    axes[2].set_xlabel("Frecuencia (Hz)", color="#cdd6f4")
    axes[2].set_ylabel("Potencia", color="#cdd6f4")
    axes[2].grid(True, linestyle="--", alpha=0.5)
    axes[2].legend()