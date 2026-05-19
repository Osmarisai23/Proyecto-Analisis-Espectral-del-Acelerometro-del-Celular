import matplotlib.pyplot as plt
import os

def crear_tabla_comparativa(resultados):

    os.makedirs("resultados",exist_ok = True)

    fig, ax = plt.subplots(figsize = (12, 3))  #Crea una figura para dibujar la tabla como imagen

    ax.axis("off") #Oculta los ejes para mostrar únicamente la tabla

    columnas = ["Actividad", "Frecuencia Dominante (Hz)", "Cadencia (pasos/min)", "Pico Máximo", "Energía Espectral"] #Encabezados que tendrá la tabla comparativa

    #Construye la tabla con los datos recibidos desde main.py
    tabla = ax.table(
        cellText = resultados, 
        colLabels = columnas, 
        cellLoc = "center", 
        loc = "center"
        )

    #Ajustes visuales para mejorar legibilidad
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(11)
    tabla.scale(1.2, 2)

    
    plt.title(
        "Tabla General Comparativa", 
        fontsize = 16, 
        fontweight = "bold", 
        pad = 20
        )

    plt.tight_layout()

    plt.savefig("resultados/tabla_comparativa.png", dpi=300, bbox_inches="tight")
    plt.show()