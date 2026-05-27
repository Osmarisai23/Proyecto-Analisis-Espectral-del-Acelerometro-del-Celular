# Plan de Desarrollo: Análisis Espectral del Acelerómetro del Celular

Referencia: Proyecto `Análisis Espectral del Acelerómetro del Celular`.  

---

## Etapa 1 — Organización del proyecto

**Objetivo:** crear una estructura ordenada para separar datos, código, imágenes y archivo principal.

### Qué implementar

Crear la siguiente estructura de carpetas:

```
ProyectoAnalisisdeAcelerometro/
│
├── Datos/
│   ├── caminar.csv
│   └── correr.csv
│
├── imagenes/
│   ├── menu_programa.jpg
│   ├── grafica_caminar.png
│   ├── grafica_correr.png
│   ├── espectrograma_caminar.png
│   ├── espectrograma_correr.png
│   ├── comparacion_caminar_correr.png
│   ├── tabla_comparativa.png
│   └── tabla_armonicos.png
│
├── scripts/
│   ├── __init__.py
│   ├── leer_datos.py
│   ├── procesar_senal.py
│   ├── fft_espectral.py
│   ├── graficar.py
│   ├── espectrograma.py
│   ├── comparar.py
│   ├── tabla_comparativa.py
│   └── tabla_armonicos.py
│
└── main.py

```

### Puntos críticos

* La carpeta `Datos` debe contener los archivos `caminar.csv` y `correr.csv`.
* La carpeta `scripts` debe incluir `__init__.py` para mantener una estructura modular.
* El archivo `main.py` debe estar en la raíz del proyecto.
* No modificar manualmente la carpeta `__pycache__`, ya que Python la genera automáticamente.

### Hito

Verificar que el proyecto tenga la estructura correcta y que los archivos CSV estén disponibles en la carpeta `Datos`.

---

## Etapa 2 — `leer_datos.py`

**Objetivo:** leer los archivos CSV del acelerómetro y separar los datos principales.

### Qué implementar

Función `leer_datos(archivo)`.

Debe leer el archivo CSV y separar:

* Tiempo.
* Aceleración en X.
* Aceleración en Y.
* Aceleración en Z.

### Implementación base

```python
import pandas as pd

def leer_datos(archivo):

    df = pd.read_csv(archivo)

    t = df.iloc[:,0].values
    ax = df.iloc[:,1].values
    ay = df.iloc[:,2].values
    az = df.iloc[:,3].values

    return t, ax, ay, az
```

### Puntos críticos

* El archivo CSV debe tener al menos cuatro columnas.
* La primera columna debe representar el tiempo.
* Las siguientes tres columnas deben representar las aceleraciones en X, Y y Z.
* Si el archivo no tiene el formato esperado, el análisis no será correcto.

### Hito

Ejecutar una prueba rápida:

```python
from scripts.leer_datos import leer_datos

t, ax, ay, az = leer_datos("Datos/caminar.csv")

print(t[:5])
print(ax[:5])
print(ay[:5])
print(az[:5])
```

Debe imprimir los primeros valores de tiempo y aceleración sin errores.

---

## Etapa 3 — `procesar_senal.py`

**Objetivo:** convertir las tres señales del acelerómetro en una sola señal útil para el análisis espectral.

### Qué implementar

Función `procesar_senal(ax, ay, az)`.

Debe realizar dos procesos:

1. Calcular la magnitud vectorial.
2. Eliminar la componente DC.

### Implementación base

```python
import numpy as np

def procesar_senal(ax, ay, az):

    magnitud = np.sqrt(ax**2 + ay**2 + az**2)

    magnitud_ac = magnitud - np.mean(magnitud)

    return magnitud_ac
```

### Puntos críticos

* La magnitud vectorial combina los tres ejes en una sola señal.
* Restar el promedio elimina la componente DC.
* La señal resultante debe quedar centrada alrededor de cero.

### Hito

Ejecutar:

```python
from scripts.leer_datos import leer_datos
from scripts.procesar_senal import procesar_senal

t, ax, ay, az = leer_datos("Datos/caminar.csv")
senal = procesar_senal(ax, ay, az)

print(senal[:10])
print("Promedio:", senal.mean())
```

El promedio debe estar cercano a cero.

---

## Etapa 4 — `fft_espectral.py`

**Objetivo:** aplicar análisis espectral a la señal procesada y obtener las métricas principales.

### Qué implementar

Función `fft_espectral(senal, tiempo)`.

Debe calcular:

* Frecuencia de muestreo.
* FFT.
* Espectro de un solo lado.
* Frecuencia dominante.
* Cadencia.
* Pico máximo.
* Energía espectral.
* Densidad espectral de potencia.

### Implementación base

```python
import numpy as np
from scipy.signal import welch

def fft_espectral(senal, tiempo):

    dt = np.mean(np.diff(tiempo))
    fs = 1 / dt

    N = len(senal)

    ventana = np.hanning(N)
    senal_window = senal * ventana

    Y = np.fft.fft(senal_window)

    P1 = np.abs(Y/N)
    P1 = P1[:N//2 + 1]
    P1[1:-1] *= 2

    f = np.fft.fftfreq(N, d=dt)
    f = f[:N//2 + 1]

    frecuencia_dom = f[np.argmax(P1)]

    cadencia = frecuencia_dom * 60

    pico_max = np.max(np.abs(senal))

    energia_espectral = np.sum(P1**2)

    f_psd, psd = welch(senal, fs=fs, nperseg=256)

    return f, P1, frecuencia_dom, cadencia, pico_max, energia_espectral, f_psd, psd
```

### Puntos críticos

* La frecuencia de muestreo se calcula usando el vector de tiempo.
* La ventana Hann reduce fugas espectrales.
* La FFT permite obtener el contenido de frecuencia.
* La frecuencia dominante se obtiene buscando el valor máximo del espectro.
* La cadencia se calcula como `frecuencia_dom * 60`.
* La PSD se calcula usando el método de Welch.

### Hito

Ejecutar:

```python
from scripts.leer_datos import leer_datos
from scripts.procesar_senal import procesar_senal
from scripts.fft_espectral import fft_espectral

t, ax, ay, az = leer_datos("Datos/caminar.csv")
senal = procesar_senal(ax, ay, az)

f, P1, fd, cad, pico, energia, f_psd, psd = fft_espectral(senal, t)

print("Frecuencia dominante:", fd)
print("Cadencia:", cad)
print("Pico máximo:", pico)
print("Energía espectral:", energia)
```

Debe imprimir las métricas principales sin errores.

---

## Etapa 5 — `graficar.py`

**Objetivo:** generar gráficas individuales para cada actividad.

### Qué implementar

Función `graficar(...)`.

Debe mostrar:

1. Señal en el tiempo.
2. Análisis espectral FFT.
3. Densidad espectral de potencia.

### Puntos críticos

* La primera gráfica debe usar tiempo en el eje X.
* La segunda gráfica debe usar frecuencia en Hz.
* La tercera gráfica debe mostrar la PSD.
* El eje de frecuencia puede limitarse de 0 a 10 Hz porque caminar y correr se encuentran en frecuencias bajas.

### Hito

Ejecutar el análisis de una actividad y verificar visualmente que aparezcan tres gráficas:

```
1. Señal en el tiempo
2. FFT
3. PSD
```

Las gráficas deben tener títulos, ejes y datos visibles.

---

## Etapa 6 — `espectrograma.py`

**Objetivo:** visualizar cómo cambian las frecuencias de la señal a lo largo del tiempo.

### Qué implementar

Función `espectrograma(senal, t, titulo)`.

Debe calcular la frecuencia de muestreo y generar un espectrograma usando `plt.specgram`.

### Implementación base

```python
import matplotlib.pyplot as plt
import numpy as np
import os

def espectrograma(senal, t, titulo):

    dt = np.mean(np.diff(t))
    fs = 1 / dt

    plt.figure(figsize=(10,5))

    plt.specgram(
        senal,
        Fs=fs,
        NFFT=256,
        noverlap=200,
        cmap="viridis",
        vmin=-80,
        vmax=20
    )

    plt.colorbar(label="Intensidad")
    plt.ylim(0,8)

    plt.xlabel("Tiempo (s)")
    plt.ylabel("Frecuencia (Hz)")
    plt.title(f"Espectrograma - {titulo}")

    plt.tight_layout()
    os.makedirs("resultados", exist_ok=True)
    plt.savefig(f"resultados/espectrograma_{titulo.lower()}.png", dpi=300, bbox_inches="tight")
    plt.show()
```

### Puntos críticos

* El espectrograma debe usar la frecuencia de muestreo correcta.
* El eje Y se limita a 8 Hz porque las actividades analizadas tienen frecuencias bajas.
* El espectrograma permite observar cambios de frecuencia durante el tiempo.

### Hito

Generar un espectrograma para caminar y otro para correr.
Deben observarse diferencias de intensidad entre ambas actividades.

---

## Etapa 7 — `comparar.py`

**Objetivo:** comparar caminar y correr en una misma visualización.

### Qué implementar

Función `comparar(ruta_caminar, ruta_correr, fig, axes)`.

Debe procesar ambos archivos y mostrar:

1. Comparación de señal temporal.
2. Comparación FFT.
3. Comparación PSD.

### Puntos críticos

* Ambas actividades deben procesarse con el mismo flujo.
* Las gráficas deben incluir etiquetas para distinguir caminar y correr.
* Se debe limpiar la figura antes de dibujar una nueva comparación.
* El eje de frecuencia debe limitarse para observar mejor el rango útil.

### Hito

Ejecutar la comparación y verificar que aparezcan las dos actividades en la misma figura:

```
Caminar vs Correr
```

Debe observarse que correr presenta mayor amplitud, frecuencia y potencia.

---

## Etapa 8 — `tabla_comparativa.py`

**Objetivo:** organizar las métricas principales en una tabla.

### Qué implementar

Función `crear_tabla_comparativa(resultados)`.

Debe generar una tabla con:

* Actividad.
* Frecuencia dominante.
* Cadencia.
* Pico máximo.
* Energía espectral.

### Implementación base

```python
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
```

### Puntos críticos

* Los resultados deben estar previamente calculados.
* Los valores deben redondearse para facilitar la lectura.
* La tabla debe permitir comparar caminar y correr fácilmente.

### Hito

Generar la tabla comparativa y verificar que muestre:

```
Frecuencia dominante
Cadencia
Pico máximo
Energía espectral
```

---

## Etapa 9 — `tabla_armonicos.py`

**Objetivo:** calcular los armónicos de la frecuencia fundamental de cada actividad.

### Qué implementar

Función `crear_tabla_armonicos(resultados)`.

Debe calcular:

```
f, 2f, 3f, 4f, 5f, 6f
```

para caminar y correr.

### Implementación base

```python
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
```

### Puntos críticos

* La frecuencia dominante se toma como frecuencia fundamental.
* Los armónicos son múltiplos de la frecuencia fundamental.
* Correr debe mostrar armónicos más altos que caminar porque su frecuencia dominante es mayor.

### Hito

Generar la tabla de armónicos y verificar que los valores sean múltiplos de la frecuencia fundamental.

---

## Etapa 10 — `main.py`

**Objetivo:** integrar todos los módulos en una interfaz gráfica funcional.

### Qué implementar

Crear una interfaz con Tkinter que permita:

* Cargar CSV de caminar.
* Cargar CSV de correr.
* Mostrar gráficas individuales.
* Mostrar espectrogramas.
* Mostrar comparación cruzada.
* Generar tabla comparativa.
* Generar tabla de armónicos.
* Mostrar historial de métricas.

### Puntos críticos

* Validar que el usuario cargue los archivos antes de generar resultados.
* Guardar los resultados en un diccionario para reutilizarlos.
* Limpiar el lienzo antes de dibujar nuevas gráficas.
* Integrar Matplotlib correctamente dentro de Tkinter.
* Mostrar mensajes de error si faltan archivos.

### Hito

Ejecutar:

```bash
python main.py
```

Después verificar que la interfaz permita:

```text
1. Cargar caminar.csv
2. Cargar correr.csv
3. Ver gráficas individuales
4. Ver espectrogramas
5. Mostrar comparación cruzada
6. Generar tabla comparativa
7. Generar tabla de armónicos
```

---

## Etapa 11 — Resultados y capturas

**Objetivo:** documentar los resultados obtenidos para el reporte técnico.

### Qué generar

Capturas de:

* Interfaz principal.
* Gráfica individual de caminar.
* Gráfica individual de correr.
* Espectrograma de caminar.
* Espectrograma de correr.
* Comparación caminar vs correr.
* Tabla comparativa.
* Tabla de armónicos.

### Puntos críticos

* Las capturas deben ser claras.
* Las imágenes deben guardarse en la carpeta `imagenes`.
* Los nombres de archivo deben coincidir con los usados en el reporte.

### Hito

Verificar que existan los siguientes archivos:

```
imagenes/menu_programa.jpg
imagenes/grafica_caminar.png
imagenes/grafica_correr.png
imagenes/espectrograma_caminar.png
imagenes/espectrograma_correr.png
imagenes/comparacion_caminar_correr.png
imagenes/tabla_comparativa.png
imagenes/tabla_armonicos.png
```

---

## Etapa 12 — Reporte técnico y README

**Objetivo:** documentar el proyecto para entrega académica y repositorio de GitHub.

### Qué implementar

Crear:

* `README.md`
* Reporte técnico en Markdown

El reporte debe incluir:

* Datos generales.
* Introducción.
* Objetivos.
* Marco teórico.
* Estructura del proyecto.
* Librerías utilizadas.
* Descripción de módulos.
* Análisis del código.
* Metodología.
* Resultados.
* Interpretación.
* Validación.
* Conclusiones.
* Anexo de resultados.

### Puntos críticos

* El README debe ser breve y claro.
* El reporte debe explicar el funcionamiento y los resultados.
* Las imágenes deben insertarse correctamente desde la carpeta `imagenes`.
* Los resultados numéricos deben coincidir con los obtenidos por el programa.

### Hito

Verificar que el proyecto tenga:

```
README.md
Reporte técnico
imagenes/
Datos/
scripts/
main.py
```

---

## Resumen de hitos

| Etapa | Archivo o sección      | Hito verificable                                            |
| ----- | ---------------------- | ----------------------------------------------------------- |
| 1     | Estructura             | Carpetas `Datos`, `scripts`, `imagenes` y `main.py` creados |
| 2     | `leer_datos.py`        | CSV leído correctamente y columnas separadas                |
| 3     | `procesar_senal.py`    | Señal de magnitud sin componente DC                         |
| 4     | `fft_espectral.py`     | Frecuencia dominante, cadencia, pico y energía calculados   |
| 5     | `graficar.py`          | Gráficas individuales generadas                             |
| 6     | `espectrograma.py`     | Espectrogramas de caminar y correr generados                |
| 7     | `comparar.py`          | Comparación caminar vs correr visible                       |
| 8     | `tabla_comparativa.py` | Tabla de métricas generada                                  |
| 9     | `tabla_armonicos.py`   | Tabla de armónicos generada                                 |
| 10    | `main.py`              | Interfaz gráfica funcional                                  |
| 11    | Resultados             | Capturas guardadas en `imagenes`                            |
| 12    | Documentación          | README y reporte técnico terminados                         |

