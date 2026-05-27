import pandas as pd

def leer_datos(archivo):

    #Lectura del archivo CSV indicado desde main.py
    df = pd.read_csv(archivo)

    # Separación de columnas:
    # tiempo, aceleración en X, aceleración en Y y aceleración en Z
    t = df.iloc[:,0].values
    ax = df.iloc[:,1].values
    ay = df.iloc[:,2].values
    az = df.iloc[:,3].values

    return t, ax, ay, az