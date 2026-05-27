import numpy as np
from scipy.signal import welch

def fft_espectral(senal, tiempo):

    #Cálculo de frecuencia de muestreo usando el vector de tiempo
    dt = np.mean(np.diff(tiempo))
    fs = 1 / dt

    N = len(senal)

    #Ventana Hann para reducir fugas espectrales antes de aplicar FFT
    ventana = np.hanning(N)
    senal_window = senal * ventana
    
    Y = np.fft.fft(senal_window) #Transformada Rápida de Fourier

    #Magnitud del espectro de un solo lado
    P1 = np.abs(Y/N)
    P1 = P1[:N//2 + 1]
    P1[1:-1] *= 2

    #Vector de frecuencias asociado al espectro
    f = np.fft.fftfreq(N, d=dt)
    f = f[:N//2 + 1]

    frecuencia_dom = f[np.argmax(P1)] #Obtiene la frecuencia con mayor magnitud en el espectro
    
    cadencia = frecuencia_dom * 60  #Conversión de Hz a pasos por minuto aproximados

    pico_max = np.max(np.abs(senal)) #Obtiene la máxima amplitud registrada en la señal procesada
    
    energia_espectral = np.sum(P1**2) # calcula la energía total del espectro
    
    f_psd, psd = welch(senal, fs=fs, nperseg=256) #Densidad espectral de potencia usando Welch
    
    return f, P1, frecuencia_dom, cadencia, pico_max, energia_espectral, f_psd, psd