from scripts.leer_datos import leer_datos
from scripts.procesar_senal import procesar_senal
from scripts.fft_espectral import fft_espectral
from scripts.graficar import graficar
from scripts.comparar import comparar
from scripts.espectrograma import espectrograma
from scripts.tabla_comparativa import crear_tabla_comparativa
from scripts.tabla_armonicos import crear_tabla_armonicos

def analizar_archivo(archivo, titulo):

    print("\nAnalizando:", archivo)

    t, ax, ay, az = leer_datos(archivo) #Lectura del archivo CSV y separación de ejes del acelerómetro

    senal = procesar_senal(ax, ay, az) #Procesamiento de la señal: magnitud vectorial y eliminación de DC

    (f, P1, frecuencia_dom, cadencia, pico_max, energia_espectral, f_psd, psd) = fft_espectral(senal, t) #Análisis espectral y cálculo de métricas principales

    #Resultados principales en consola
    print(f"Frecuencia dominante: " f"{frecuencia_dom:.2f} Hz")
    print(f"Cadencia estimada: " f"{cadencia:.2f} pasos/min")
    print(f"Pico máximo: " f"{pico_max:.2f}")
    print(f"Energía espectral: " f"{energia_espectral:.2f}")

    graficar(t, senal, f, P1, frecuencia_dom, cadencia, f_psd, psd, titulo) #Gráficas individuales: tiempo, FFT y PSD

    espectrograma(senal, t, titulo) #Espectrograma de la actividad

    return (frecuencia_dom, cadencia, pico_max, energia_espectral)


def main():

    #Análisis individual de cada actividad
    freq_caminar, cad_caminar, pico_caminar, energia_caminar = analizar_archivo("datos/caminar.csv", "Caminar")
    freq_correr, cad_correr, pico_correr, energia_correr = analizar_archivo("datos/correr.csv", "Correr")

    comparar()

    # Datos para la tabla general comparativa
    resultados = [
    [
        "Caminar",
        f"{freq_caminar:.2f}",
        f"{cad_caminar:.2f}",
        f"{pico_caminar:.2f}",
        f"{energia_caminar:.2f}"
    ],
    [
        "Correr",
        f"{freq_correr:.2f}",
        f"{cad_correr:.2f}",
        f"{pico_correr:.2f}",
        f"{energia_correr:.2f}"
    ]
]

    crear_tabla_comparativa(resultados)

    #Datos para la tabla de armónicos
    armonicos = [
    [
        "Caminar",
        f"{freq_caminar:.2f}",
        f"{2*freq_caminar:.2f}",
        f"{3*freq_caminar:.2f}"
    ],
    [
        "Correr",
        f"{freq_correr:.2f}",
        f"{2*freq_correr:.2f}",
        f"{3*freq_correr:.2f}"
    ]
]

    crear_tabla_armonicos(armonicos)

if __name__ == "__main__":
    main()