# Análisis Espectral del Acelerómetro del Celular

Proyecto desarrollado para la materia **Matemáticas IV** del Departamento Académico de Sistemas Computacionales (DASC), Universidad Autónoma de Baja California Sur.

El proyecto analiza datos del acelerómetro de un celular para comparar dos actividades físicas: **caminar** y **correr**.  
A partir de archivos CSV, el programa procesa la señal, aplica análisis espectral mediante FFT y muestra métricas como frecuencia dominante, cadencia, pico máximo, energía espectral, PSD, espectrogramas y armónicos.

## Estructura

```
Datos/
├── caminar.csv                    # Datos del acelerómetro registrados al caminar
└── correr.csv                     # Datos del acelerómetro registrados al correr

imagenes/
├── menu_programa.jpg              # Captura de la interfaz principal del programa
├── grafica_caminar.png            # Gráficas de señal temporal, FFT y PSD de caminar
├── grafica_correr.png             # Gráficas de señal temporal, FFT y PSD de correr
├── espectrograma_caminar.png      # Espectrograma de la actividad caminar
├── espectrograma_correr.png       # Espectrograma de la actividad correr
├── comparacion_caminar_correr.png # Comparación simultánea entre caminar y correr
├── tabla_comparativa.png          # Tabla con frecuencia, cadencia, pico y energía espectral
└── tabla_armonicos.png            # Tabla de armónicos calculados

scripts/
├── __init__.py                    # Permite reconocer scripts como paquete de Python
├── leer_datos.py                  # Lectura de archivos CSV
├── procesar_senal.py              # Magnitud vectorial y eliminación de componente DC
├── fft_espectral.py               # FFT, PSD y cálculo de métricas principales
├── graficar.py                    # Generación de gráficas individuales
├── espectrograma.py               # Generación de espectrogramas
├── comparar.py                    # Comparación entre caminar y correr
├── tabla_comparativa.py           # Creación de tabla comparativa
└── tabla_armonicos.py             # Creación de tabla de armónicos

main.py                            # Interfaz gráfica principal del proyecto
```
Consultar el reporte técnico para la explicación completa del desarrollo, metodología, resultados e interpretación.

## Instalación

```bash
pip install numpy pandas matplotlib scipy 
```
`tkinter` normalmente viene incluido con Python.

## Uso

Ejecutar el programa principal:

```bash
python main.py
```

Dentro de la interfaz:

```text
1. Cargar Datos/caminar.csv
2. Cargar Datos/correr.csv
3. Visualizar gráficas individuales
4. Generar espectrogramas
5. Mostrar comparación cruzada
6. Generar tabla comparativa
7. Generar tabla de armónicos
```

## Resultados principales

| Actividad | Frecuencia dominante (Hz) | Cadencia (pasos/min) | Pico máximo | Energía espectral |
| --------- | ------------------------: | -------------------: | ----------: | ----------------: |
| Caminar   |                      1.65 |                 98.8 |        3.84 |              0.38 |
| Correr    |                      5.48 |                328.8 |       41.37 |             63.95 |

Los resultados muestran que correr genera una señal con mayor frecuencia dominante, mayor amplitud y mayor energía espectral que caminar.

## Licencia

Uso académico.