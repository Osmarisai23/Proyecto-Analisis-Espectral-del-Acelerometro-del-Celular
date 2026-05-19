
# Plan de Desarrollo: ProyectoAnalisisdeAcelerometro

Referencia: análisis espectral de datos del acelerómetro del celular.  
Cada etapa produce un hito verificable antes de continuar con la siguiente. **No se avanza si el hito no pasa.**

---

## Etapa 1 — Organización del proyecto

**Objetivo:** preparar una estructura clara para separar el archivo principal, los datos, los módulos de procesamiento y los resultados.

### Qué implementar

Estructura base del proyecto:

```text
ProyectoAnalisisdeAcelerometro/
│
├── datos/
│   ├── caminar.csv
│   └── correr.csv
│
├── scripts/
│   ├── __init__.py
│   ├── leer_datos.py
│   ├── procesar_senal.py
│   ├── fft_espectral.py
│   ├── graficar.py
│   ├── comparar.py
│   ├── espectrograma.py
│   ├── tabla_comparativa.py
│   └── tabla_armonicos.py
│
├── resultados/
│   ├── comparacion_caminar_correr.png
│   ├── espectrograma_caminar.png
│   ├── espectrograma_correr.png
│   ├── graficas_caminar.png
│   ├── graficas_correr.png
│   ├── tabla_armonicos.png
│   └── tabla_comparativa.png
│
├── main.py
├── PlanC.md
├── README.md
└── REPORTE.md
````

### Puntos críticos

* La carpeta `scripts/` debe incluir `__init__.py`, aunque esté vacío.
* Los archivos `caminar.csv` y `correr.csv` deben estar dentro de `datos/`.
* Las imágenes generadas por el programa deben guardarse en `resultados/`.
* Los nombres de archivos deben coincidir con las rutas usadas en el código.

### Hito

Ejecutar en consola:

```bash
python main.py
```

Resultado esperado: el programa debe iniciar sin errores de importación.
Si aparece un error como `ModuleNotFoundError`, revisar que la carpeta `scripts/` tenga `__init__.py` y que los nombres de archivos coincidan.

---

## Etapa 2 — Registro de datos del acelerómetro

**Objetivo:** obtener datos reales de movimiento usando el acelerómetro del celular.

### Qué implementar

Registrar dos actividades:

* Caminar.
* Correr.

Herramientas usadas:

* **Physics Toolbox Sensor Suite** para registrar los datos del acelerómetro.
* **Visual Studio Code** para escribir y ejecutar el código.
* **Python** para procesar, analizar y graficar los datos.

Cada prueba tiene una duración aproximada de **42 segundos**.

### Puntos críticos

* Los datos deben exportarse en formato `.csv`.
* El programa usa las primeras cuatro columnas del archivo:

  * Tiempo.
  * Aceleración en X.
  * Aceleración en Y.
  * Aceleración en Z.
* Los archivos deben llamarse exactamente `caminar.csv` y `correr.csv`.

### Hito

Verificar que existan los archivos:

```text
datos/caminar.csv
datos/correr.csv
```

Ejecutar una revisión rápida desde Python:

```python
import pandas as pd

df_caminar = pd.read_csv("datos/caminar.csv")
df_correr = pd.read_csv("datos/correr.csv")

print(df_caminar.shape)
print(df_correr.shape)
# esperado: ambos archivos deben tener filas de datos y al menos 4 columnas
```

---

## Etapa 3 — `leer_datos.py`

**Objetivo:** leer los archivos CSV y separar las columnas necesarias para el análisis.

### Qué implementar

Función `leer_datos(archivo)` que lea un archivo CSV y retorne:

* `t`: tiempo.
* `ax`: aceleración en X.
* `ay`: aceleración en Y.
* `az`: aceleración en Z.

### Fragmento clave

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

* El archivo debe existir en la ruta indicada.
* El CSV debe tener al menos cuatro columnas.
* El código usa `iloc`, por lo que toma las columnas por posición.
* El orden esperado es: tiempo, aceleración X, aceleración Y y aceleración Z.

### Hito

Ejecutar en consola o en un archivo de prueba:

```python
from scripts.leer_datos import leer_datos

t, ax, ay, az = leer_datos("datos/caminar.csv")

print(len(t), len(ax), len(ay), len(az))
# esperado: los cuatro valores deben ser iguales
```

Si los tamaños no coinciden, revisar el archivo CSV.

---

## Etapa 4 — `procesar_senal.py`

**Objetivo:** convertir los tres ejes del acelerómetro en una sola señal útil para el análisis.

### Qué implementar

Función `procesar_senal(ax, ay, az)` que calcule la magnitud vectorial y elimine la componente DC.

### Fragmento clave

```python
import numpy as np

def procesar_senal(ax, ay, az):

    magnitud = np.sqrt(ax**2 + ay**2 + az**2)

    magnitud_ac = magnitud - np.mean(magnitud)

    return magnitud_ac
```

### Puntos críticos

* La magnitud permite trabajar con una sola señal en lugar de tres ejes separados.
* Eliminar la componente DC evita que la frecuencia de 0 Hz domine la FFT.
* La señal resultante debe quedar centrada alrededor de cero.

### Hito

Ejecutar:

```python
from scripts.leer_datos import leer_datos
from scripts.procesar_senal import procesar_senal

t, ax, ay, az = leer_datos("datos/caminar.csv")
senal = procesar_senal(ax, ay, az)

print(senal.mean())
# esperado: un valor cercano a 0
```

Si el promedio no está cerca de cero, revisar la resta del promedio en `procesar_senal.py`.

---

## Etapa 5 — `fft_espectral.py`

**Objetivo:** transformar la señal del dominio del tiempo al dominio de la frecuencia para identificar patrones de movimiento.

### Qué implementar

Función `fft_espectral(senal, tiempo)` que calcule:

* Frecuencia de muestreo.
* Ventana Hann.
* FFT de un solo lado.
* Frecuencia dominante.
* Cadencia estimada.
* Pico máximo.
* Energía espectral.
* Densidad espectral de potencia usando Welch.

### Fragmento clave

```python
dt = np.mean(np.diff(tiempo))
fs = 1 / dt

N = len(senal)

ventana = np.hanning(N)
senal_window = senal * ventana

Y = np.fft.fft(senal_window)
```

Este bloque calcula la frecuencia de muestreo, aplica la ventana Hann y obtiene la FFT.

```python
P1 = np.abs(Y/N)
P1 = P1[:N//2 + 1]
P1[1:-1] *= 2

f = np.fft.fftfreq(N, d=dt)
f = f[:N//2 + 1]
```

Este bloque obtiene el espectro de un solo lado y su vector de frecuencias.

```python
frecuencia_dom = f[np.argmax(P1)]

cadencia = frecuencia_dom * 60

pico_max = np.max(np.abs(senal))

energia_espectral = np.sum(P1**2)

f_psd, psd = welch(senal, fs=fs, nperseg=256)
```

Este bloque calcula las métricas principales del proyecto.

### Puntos críticos

* La frecuencia de muestreo se calcula con el vector de tiempo.
* La ventana Hann reduce fugas espectrales.
* La frecuencia dominante indica el ritmo principal del movimiento.
* La cadencia se estima multiplicando la frecuencia dominante por 60.
* La PSD permite observar cómo se distribuye la potencia de la señal.

### Hito

Ejecutar:

```python
from scripts.leer_datos import leer_datos
from scripts.procesar_senal import procesar_senal
from scripts.fft_espectral import fft_espectral

t, ax, ay, az = leer_datos("datos/caminar.csv")
senal = procesar_senal(ax, ay, az)

f, P1, frecuencia_dom, cadencia, pico_max, energia_espectral, f_psd, psd = fft_espectral(senal, t)

print(f"Frecuencia dominante: {frecuencia_dom:.2f} Hz")
print(f"Cadencia estimada: {cadencia:.2f} pasos/min")
print(f"Pico máximo: {pico_max:.2f}")
print(f"Energía espectral: {energia_espectral:.2f}")
```

Resultado esperado para caminar:

```text
Frecuencia dominante: 1.65 Hz
Cadencia estimada: 98.80 pasos/min
Pico máximo: 3.84
Energía espectral: 0.38
```

---

## Etapa 6 — `graficar.py`

**Objetivo:** representar cada actividad en el dominio del tiempo y de la frecuencia.

### Qué implementar

Función `graficar(...)` para generar tres gráficas por actividad:

1. Señal en el tiempo.
2. Espectro de frecuencias mediante FFT.
3. Densidad espectral de potencia.

### Fragmento clave

```python
fig, axes = plt.subplots(3, 1, figsize = (10, 10))
fig.suptitle(titulo, fontsize = 16, fontweight = "bold")

axes[0].plot(t, senal, "black")
axes[0].set_title("Señal en el tiempo")

axes[1].plot(f, P1, "royalblue")
axes[1].axvline(frecuencia_dom, color = "red", linestyle = "--")
axes[1].set_xlim(0, 10)

axes[2].semilogy(f_psd, psd)
axes[2].set_xlim(0, 10)
```

Este bloque genera las gráficas de tiempo, FFT y PSD. La línea roja marca la frecuencia dominante.

```python
os.makedirs("resultados", exist_ok=True)
plt.savefig(f"resultados/graficas_{titulo.lower()}.png", dpi=300, bbox_inches="tight")
```

Este bloque guarda la gráfica generada dentro de la carpeta `resultados/`.

### Puntos críticos

* La gráfica FFT debe marcar la frecuencia dominante.
* El eje de frecuencia se limita de 0 a 10 Hz porque caminar y correr son movimientos de baja frecuencia.
* El archivo debe guardarse antes de `plt.show()`.

### Hito

Ejecutar:

```bash
python main.py
```

Verificar que se generen:

```text
resultados/graficas_caminar.png
resultados/graficas_correr.png
```

Si no aparecen, revisar que `plt.savefig(...)` esté antes de `plt.show()`.

---

## Etapa 7 — `espectrograma.py`

**Objetivo:** observar cómo cambia la frecuencia de la señal durante el tiempo.

### Qué implementar

Función `espectrograma(senal, t, titulo)` que genere un espectrograma para cada actividad.

### Fragmento clave

```python
dt = np.mean(np.diff(t))
fs = 1 / dt

plt.specgram(
    senal,
    Fs=fs,
    NFFT = 256,
    noverlap = 200,
    cmap = "viridis",
    vmin = -80,
    vmax = 20
)

plt.ylim(0,8)
```

Este bloque calcula la frecuencia de muestreo y genera el espectrograma.

```python
os.makedirs("resultados", exist_ok=True)
plt.savefig(f"resultados/espectrograma_{titulo.lower()}.png", dpi=300, bbox_inches="tight")
```

Este bloque guarda el espectrograma correspondiente a cada actividad.

### Puntos críticos

* El espectrograma permite observar cambios de frecuencia durante el tiempo.
* Se limita a 8 Hz porque caminar y correr se encuentran principalmente en frecuencias bajas.
* El archivo debe llamarse según la actividad: `espectrograma_caminar.png` o `espectrograma_correr.png`.

### Hito

Ejecutar:

```bash
python main.py
```

Verificar que se generen:

```text
resultados/espectrograma_caminar.png
resultados/espectrograma_correr.png
```

---

## Etapa 8 — `comparar.py`

**Objetivo:** comparar caminar y correr usando la señal temporal, la FFT y la PSD.

### Qué implementar

Función `comparar()` que:

* Lea los archivos `caminar.csv` y `correr.csv`.
* Procese ambas señales.
* Calcule FFT y PSD.
* Genere una figura comparativa.

### Fragmento clave

```python
archivos = {
    "Caminar": "datos/caminar.csv",
    "Correr": "datos/correr.csv"
}

datos = {}

for actividad, archivo in archivos.items():

    t, ax, ay, az = leer_datos(archivo)

    senal = procesar_senal(ax, ay, az)

    (f, P1, frecuencia_dom, cadencia, pico_max, energia_espectral, f_psd, psd) = fft_espectral(senal, t)

    datos[actividad] = {
        "t": t,
        "senal": senal,
        "f": f,
        "P1": P1,
        "f_psd": f_psd,
        "psd": psd,
        "freq": frecuencia_dom,
        "cad": cadencia,
        "pico": pico_max,
        "energia": energia_espectral
    }
```

Este bloque carga, procesa y analiza ambas actividades para poder compararlas.

```python
for actividad in datos:
    axes[0].plot(datos[actividad]["t"], datos[actividad]["senal"], label=actividad)

for actividad in datos:
    axes[1].plot(datos[actividad]["f"], datos[actividad]["P1"], label=actividad)

for actividad in datos:
    axes[2].semilogy(datos[actividad]["f_psd"], datos[actividad]["psd"], label=actividad)
```

Este bloque dibuja la comparación temporal, la comparación por FFT y la comparación por PSD.

```python
os.makedirs("resultados", exist_ok=True)
plt.savefig("resultados/comparacion_caminar_correr.png", dpi=300, bbox_inches="tight")
```

Este bloque guarda la figura comparativa.

### Puntos críticos

* Correr debe mostrar mayor energía espectral que caminar.
* La frecuencia dominante de correr debe ser mayor que la de caminar.
* La comparación no debe confundirse con la tabla comparativa; esta imagen corresponde a una gráfica.

### Hito

Ejecutar:

```bash
python main.py
```

Verificar que se genere:

```text
resultados/comparacion_caminar_correr.png
```

---

## Etapa 9 — `tabla_comparativa.py` y `tabla_armonicos.py`

**Objetivo:** resumir los resultados principales en imágenes para documentar el proyecto.

### Qué implementar

Crear dos tablas:

1. Tabla comparativa con frecuencia dominante, cadencia, pico máximo y energía espectral.
2. Tabla de armónicos con frecuencia fundamental, `2f` y `3f`.

### Fragmento clave

Para la tabla comparativa:

```python
columnas = [
    "Actividad",
    "Frecuencia Dominante (Hz)",
    "Cadencia (pasos/min)",
    "Pico Máximo",
    "Energía Espectral"
]

tabla = ax.table(
    cellText = resultados,
    colLabels = columnas,
    cellLoc = "center",
    loc = "center"
)

plt.savefig("resultados/tabla_comparativa.png", dpi=300, bbox_inches="tight")
```

Para la tabla de armónicos:

```python
columnas = ["Actividad", "Fundamental (Hz)", "Armónico 1 (2f)", "Armónico 2 (3f)"]

tabla = ax.table(
    cellText = datos_armonicos,
    colLabels = columnas,
    cellLoc = "center",
    loc = "center"
)

plt.savefig("resultados/tabla_armonicos.png", dpi = 300, bbox_inches = "tight")
```

### Puntos críticos

* Las tablas deben guardarse dentro de `resultados/`.
* La tabla comparativa resume los valores principales de caminar y correr.
* La tabla de armónicos usa la frecuencia dominante como frecuencia fundamental.
* Solo se calculan `2f` y `3f` para mantener el análisis claro y evitar incluir frecuencias poco relevantes o ruido.

### Hito

Ejecutar:

```bash
python main.py
```

Verificar que se generen:

```text
resultados/tabla_comparativa.png
resultados/tabla_armonicos.png
```

---

## Etapa 10 — `main.py`

**Objetivo:** unir todos los módulos en un solo flujo de ejecución.

### Qué implementar

El archivo principal debe:

1. Analizar `datos/caminar.csv`.
2. Analizar `datos/correr.csv`.
3. Mostrar resultados en consola.
4. Generar gráficas individuales.
5. Generar espectrogramas.
6. Comparar caminar contra correr.
7. Crear la tabla comparativa.
8. Crear la tabla de armónicos.

### Fragmento clave

```python
def analizar_archivo(archivo, titulo):

    print("\nAnalizando:", archivo)

    t, ax, ay, az = leer_datos(archivo)

    senal = procesar_senal(ax, ay, az)

    (f, P1, frecuencia_dom, cadencia, pico_max, energia_espectral, f_psd, psd) = fft_espectral(senal, t)

    print(f"Frecuencia dominante: " f"{frecuencia_dom:.2f} Hz")
    print(f"Cadencia estimada: " f"{cadencia:.2f} pasos/min")
    print(f"Pico máximo: " f"{pico_max:.2f}")
    print(f"Energía espectral: " f"{energia_espectral:.2f}")

    graficar(t, senal, f, P1, frecuencia_dom, cadencia, f_psd, psd, titulo)

    espectrograma(senal, t, titulo)

    return (frecuencia_dom, cadencia, pico_max, energia_espectral)
```

Este bloque integra lectura, procesamiento, análisis espectral, gráficas y espectrograma para una actividad.

```python
freq_caminar, cad_caminar, pico_caminar, energia_caminar = analizar_archivo("datos/caminar.csv", "Caminar")
freq_correr, cad_correr, pico_correr, energia_correr = analizar_archivo("datos/correr.csv", "Correr")

comparar()
```

Este bloque ejecuta el análisis de ambas actividades y genera la comparación.

```python
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
```

Este bloque organiza los resultados principales y genera la tabla comparativa.

```python
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
```

Este bloque calcula los armónicos principales de cada actividad y genera la tabla correspondiente.

### Puntos críticos

* Las rutas deben coincidir con la estructura del proyecto.
* Todos los módulos deben importarse correctamente desde `scripts/`.
* La ejecución completa debe generar resultados numéricos e imágenes.
* No debe existir una tabla duplicada; solo se conserva `tabla_comparativa.png`.

### Hito

Ejecutar:

```bash
python main.py
```

Resultado esperado en consola:

```
Analizando: datos/caminar.csv
* Frecuencia dominante
- Cadencia estimada
- Pico máximo
- Energía espectral

Analizando: datos/correr.csv
- Frecuencia dominante
- Cadencia estimada
- Pico máximo
- Energía espectral
```

También deben generarse estos archivos:

```text
resultados/comparacion_caminar_correr.png
resultados/espectrograma_caminar.png
resultados/espectrograma_correr.png
resultados/graficas_caminar.png
resultados/graficas_correr.png
resultados/tabla_armonicos.png
resultados/tabla_comparativa.png
```

---

## Resumen de hitos

| Etapa | Archivo o carpeta                             | Hito verificable                                                    |
| ----- | --------------------------------------------- | ------------------------------------------------------------------- |
| 1     | Estructura general                            | El proyecto ejecuta sin errores de importación                      |
| 2     | `datos/`                                      | Existen `caminar.csv` y `correr.csv` con al menos 4 columnas        |
| 3     | `leer_datos.py`                               | Se leen correctamente tiempo, ax, ay y az                           |
| 4     | `procesar_senal.py`                           | La señal procesada queda centrada cerca de cero                     |
| 5     | `fft_espectral.py`                            | Se calculan frecuencia dominante, cadencia, pico y energía          |
| 6     | `graficar.py`                                 | Se generan `graficas_caminar.png` y `graficas_correr.png`           |
| 7     | `espectrograma.py`                            | Se generan espectrogramas por actividad                             |
| 8     | `comparar.py`                                 | Se genera `comparacion_caminar_correr.png`                          |
| 9     | `tabla_comparativa.py` y `tabla_armonicos.py` | Se generan `tabla_comparativa.png` y `tabla_armonicos.png`          |
| 10    | `main.py`                                     | Se ejecuta el flujo completo y se obtienen los resultados esperados |


