def crear_tabla_armonicos(resultados):
    datos_armonicos = []

    for actividad in ["Caminar", "Correr"]:
        res = resultados[actividad]
        fundamental = res["fd"]

        fila = [
            actividad,
            f"{fundamental:.2f}",
            f"{fundamental * 2:.2f}",
            f"{fundamental * 3:.2f}",
            f"{fundamental * 4:.2f}",
            f"{fundamental * 5:.2f}",
            f"{fundamental * 6:.2f}"
        ]

        datos_armonicos.append(fila)

    columnas = [
        "Actividad",
        "Fundamental (Hz)",
        "Armónico 1 (2f)",
        "Armónico 2 (3f)",
        "Armónico 3 (4f)",
        "Armónico 4 (5f)",
        "Armónico 5 (6f)"
    ]

    return datos_armonicos, columnas