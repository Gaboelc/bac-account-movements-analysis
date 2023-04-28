import pandas as pd
import sqlite3
import os

# Leer los archivos CSV y combinarlos en una sola tabla
dfs = []
for filename in os.listdir("data"):
    if filename.endswith(".csv"):
        filepath = os.path.join("data", filename)
        df = pd.read_csv(filepath, skiprows=4, delimiter=",", encoding="ISO-8859-1")
        # Eliminar todas las filas a partir de encontrar "Resumen de Estado Bancario" en la columna "Fecha de Transacción"
        index_to_drop = df.index[df["Fecha de Transacción"] == "Resumen de Estado Bancario"]
        if len(index_to_drop) > 0:
            df = df.iloc[:index_to_drop[0]]
        dfs.append(df)
df = pd.concat(dfs)

conn = sqlite3.connect("transacciones_bancarias.db")

df.to_sql("transacciones", conn, if_exists="replace")

conn.close()
