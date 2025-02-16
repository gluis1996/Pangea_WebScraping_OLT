import os
import datetime
import pandas as pd

# Leer la ruta base desde un archivo Excel
# excel_path = "config.xlsx"  # Cambia esto con la ruta de tu archivo Excel
# df = pd.read_excel(excel_path)
ruta_base = 'descargados'  # Suponiendo que la ruta está en la primera fila bajo la columna "Ruta"

# Obtener fecha actual en formato día-mes-año (con año en dos dígitos)
# fecha_actual = datetime.datetime.now()
fecha_actual = datetime.datetime(2025, 2, 13, 18, 0, 0)
formato_fecha = fecha_actual.strftime("%d-%m-%y")
hora_actual = fecha_actual.strftime("%H-%M-%S")  # Para reguardo

# Definir carpeta principal de la fecha
ruta_fecha = os.path.join(ruta_base, formato_fecha)

# Determinar si es antes o después de las 6 PM
hora_del_dia = fecha_actual.hour
if hora_del_dia < 15:  # Antes de las 6:00 PM se guarda en "inicio"
    periodo = "inicio"
else:  # A partir de las 6:00 PM se guarda en "final"
    periodo = "final"

# Ruta de la carpeta donde se debe guardar
ruta_periodo = os.path.join(ruta_fecha, periodo)

# Si la carpeta de la sesión ya tiene archivos, se debe guardar en 'reguardo'
if os.path.exists(ruta_periodo) and any(os.listdir(ruta_periodo)):  # Verifica si la carpeta tiene archivos
    ruta_reguardo = os.path.join(ruta_periodo, "reguardo", f"{fecha_actual.strftime('%d-%m-%y_%H-%M-%S')}")
    os.makedirs(ruta_reguardo, exist_ok=True)
    ruta_final = ruta_reguardo  # Guarda en la nueva carpeta de reguardo
else:
    os.makedirs(ruta_periodo, exist_ok=True)
    ruta_final = ruta_periodo  # Guarda en la carpeta normal
print(ruta_final)
# # Simulación de guardado de archivo
# archivo_nombre = "archivo.txt"
# ruta_archivo = os.path.join(ruta_final, archivo_nombre)

# with open(ruta_archivo, "w") as f:
#     f.write("Este es un archivo de prueba.")

# print(f"Archivo guardado en: {ruta_archivo}")
