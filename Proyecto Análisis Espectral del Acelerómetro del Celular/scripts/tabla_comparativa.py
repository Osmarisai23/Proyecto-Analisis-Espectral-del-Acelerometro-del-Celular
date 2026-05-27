def crear_tabla_comparativa(resultados):
    datos_tabla = []

    for actividad in ["Caminar", "Correr"]:
        res = resultados[actividad]

        fila = [
            actividad,
            f"{res['fd']:.2f}",
            f"{res['cad']:.1f}",
            f"{res['pico']:.2f}",
            f"{res['en']:.2f}"
        ]

        datos_tabla.append(fila)

    columnas = [
        "Actividad",
        "Frecuencia Dominante (Hz)",
        "Cadencia (pasos/min)",
        "Pico Máximo",
        "Energía Espectral"
    ]

    return datos_tabla, columnas