import matplotlib.pyplot as plt
import numpy as np
import os
def espectrograma(senal, t, titulo):

    #Cálculo de la frecuencia de muestreo a partir del vector de tiempo
    dt = np.mean(np.diff(t))
    fs = 1 / dt

    plt.figure(figsize=(10,5))
    
    #Genera el espectrograma para observar cómo cambia la frecuencia con el tiempo
    plt.specgram(
        senal, 
        Fs=fs, 
        NFFT = 256, 
        noverlap = 200, 
        cmap = "viridis", 
        vmin = -80, 
        vmax = 20
        )
    
    plt.colorbar(label="Intensidad")
    plt.ylim(0,8) #Se limitará a 8 Hz poruqe correr y caminar tiene bajas frecuencias

    plt.xlabel("Tiempo (s)")
    plt.ylabel("Frecuencia (Hz)")
    plt.title(f"Espectrograma - {titulo}")

    plt.tight_layout()
    os.makedirs("resultados", exist_ok=True)
    plt.savefig(f"resultados/espectrograma_{titulo.lower()}.png", dpi=300, bbox_inches="tight")
    plt.show()