import matplotlib.pyplot as plt
import numpy as np
import os

def graficar(t, senal, f, P1, frecuencia_dom, cadencia, f_psd, psd, titulo
):
    #Figura con tres gráficas: tiempo, FFT y PSD
    fig, axes = plt.subplots(3, 1, figsize = (10, 10))
    fig.suptitle(titulo, fontsize = 16, fontweight = "bold")
    
    #Señal procesada en el dominio del tiempo
    axes[0].plot(t, senal, "black")
    axes[0].set_title("Señal en el tiempo")
    axes[0].set_xlabel("Tiempo (s)")
    axes[0].set_ylabel("Magnitud")
    axes[0].grid(True)

    # Espectro de frecuencias obtenido con FFT
    axes[1].plot(f, P1, "royalblue")
    
    axes[1].axvline(frecuencia_dom, color = "red", linestyle = "--")

    axes[1].set_xlim(0, 10)
    axes[1].set_title("Análisis espectral FFT")
    axes[1].set_xlabel("Frecuencia (Hz)")
    axes[1].set_ylabel("Magnitud")
    axes[1].grid(True)

    #PSD: potencia de la señal distribuida por frecuencia
    axes[2].semilogy(f_psd, psd)
    axes[2].set_xlim(0, 10)
    axes[2].set_title("Densidad espectral de potencia (PSD)")
    axes[2].set_xlabel("Frecuencia (Hz)")
    axes[2].set_ylabel("Potencia")
    axes[2].grid(True)
    
    #Ajuste de espacios para evitar que el título se encime
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    os.makedirs("resultados", exist_ok=True)
    plt.savefig(f"resultados/graficas_{titulo.lower()}.png", dpi=300, bbox_inches="tight")
    plt.show()