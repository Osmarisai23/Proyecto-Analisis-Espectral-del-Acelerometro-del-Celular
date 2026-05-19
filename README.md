# Análisis Espectral de Datos del Acelerómetro del Celular

---

# ProyectoAnalisisdeAcelerometro

Proyecto desarrollado para la materia **Matemáticas IV** de la **Universidad Autónoma de Baja California Sur**.

Este proyecto analiza datos del acelerómetro de un celular al realizar dos actividades: **caminar** y **correr**.  
Los datos fueron registrados con **Physics Toolbox Sensor Suite** y procesados en Python para obtener información en el dominio del tiempo y de la frecuencia.

El programa calcula la frecuencia dominante, cadencia estimada, pico máximo, energía espectral, densidad espectral de potencia y armónicos principales de cada actividad.

---

## Estructura


```
main.py                         # Archivo principal del proyecto

datos/
  caminar.csv                   # Datos registrados al caminar
  correr.csv                    # Datos registrados al correr

scripts/
  __init__.py                   # Permite importar los módulos de la carpeta scripts
  leer_datos.py                 # Lectura de archivos CSV
  procesar_senal.py             # Cálculo de magnitud y eliminación de componente DC
  fft_espectral.py              # Análisis espectral con FFT y PSD
  graficar.py                   # Gráficas de tiempo, FFT y PSD
  comparar.py                   # Comparación entre caminar y correr
  espectrograma.py              # Generación de espectrogramas
  tabla_comparativa.py          # Tabla general comparativa
  tabla_armonicos.py            # Tabla de armónicos

resultados/
  comparacion_caminar_correr.png
  espectrograma_caminar.png
  espectrograma_correr.png
  graficas_caminar.png
  graficas_correr.png
  tabla_armonicos.png
  tabla_comparativa.png

PlanC.md                        # Plan de desarrollo por etapas
REPORTE.md                      # Reporte técnico del proyecto
README.md                       # Descripción general del proyecto
````

Consultar `PlanC.md` para el desarrollo por etapas y `REPORTE.md` para el análisis completo de resultados.

## Herramientas utilizadas
---
* Python
* Visual Studio Code
* Physics Toolbox Sensor Suite
* NumPy
* Pandas
* Matplotlib
* SciPy

---
## Instalación

Instalar las dependencias necesarias con:

```bash
pip install numpy pandas matplotlib scipy
```

---
## Uso

Ejecutar el proyecto desde la carpeta principal:

```bash
python main.py
```

El programa procesa los archivos:

```
datos/caminar.csv
datos/correr.csv
```

Después genera resultados numéricos en consola y guarda las imágenes dentro de la carpeta `resultados/`.

---

## Resultados generados

Al ejecutar el proyecto se generan los siguientes archivos:

```
resultados/comparacion_caminar_correr.png
resultados/espectrograma_caminar.png
resultados/espectrograma_correr.png
resultados/graficas_caminar.png
resultados/graficas_correr.png
resultados/tabla_armonicos.png
resultados/tabla_comparativa.png
```

Estos archivos muestran la comparación entre caminar y correr, las gráficas individuales, los espectrogramas y las tablas de resultados principales.

---

## Descripción general del análisis


El procedimiento principal del proyecto es:

1. Leer los datos del acelerómetro desde archivos CSV.
2. Separar tiempo y aceleraciones en X, Y y Z.
3. Calcular la magnitud vectorial de la aceleración.
4. Eliminar la componente DC de la señal.
5. Aplicar FFT para obtener el contenido en frecuencia.
6. Calcular frecuencia dominante, cadencia, pico máximo y energía espectral.
7. Generar gráficas, espectrogramas y tablas comparativas.

---

## Licencia


Uso académico.
