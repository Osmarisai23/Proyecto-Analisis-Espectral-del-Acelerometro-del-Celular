import matplotlib.pyplot as plt
import os

def crear_tabla_armonicos(datos_armonicos):

    os.makedirs("resultados", exist_ok = True)

    fig, ax = plt.subplots(figsize = (10, 3))

    ax.axis("off") #Oculta los ejes para que solo se vea la tabla

    columnas = ["Actividad", "Fundamental (Hz)", "Armónico 1 (2f)", "Armónico 2 (3f)"] #Encabezados que tendrá la tabla

    #Construcción de la tabla con los datos recibidos desde main.py
    tabla = ax.table(
        cellText = datos_armonicos, 
        colLabels = columnas, 
        cellLoc = "center", 
        loc = "center")

    #Ajustes visuales de la tabla
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(11)
    tabla.scale(1.2, 2)

    plt.title("Tabla de Armónicos", fontsize = 16, fontweight = "bold", pad = 20)

    plt.tight_layout()

    plt.savefig("resultados/tabla_armonicos.png", dpi = 300, bbox_inches = "tight")

    plt.show()