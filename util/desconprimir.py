import os
import zipfile
import shutil
from datetime import datetime

def descomprimir_todos_los_zip(carpeta_zip, carpeta_salida, password=None):
    # Verificar si la carpeta de salida existe, si no, crearla
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
    
    # Recorrer todos los archivos en la carpeta
    for archivo in os.listdir(carpeta_zip):
        # Verificar si el archivo es un ZIP
        if archivo.endswith('.zip'):
            ruta_zip = os.path.join(carpeta_zip, archivo)
            print(f"Descomprimiendo: {archivo}...")

            try:
                with zipfile.ZipFile(ruta_zip, 'r') as zf:
                    if password:
                        zf.setpassword(password.encode('utf-8'))  # La contraseña debe estar en bytes
                    # Extraer en una subcarpeta con el nombre del archivo ZIP
                    # nombre_subcarpeta = os.path.splitext(archivo)[0]
                    # ruta_extraccion = os.path.join(carpeta_salida, nombre_subcarpeta)
                    zf.extractall(path=carpeta_salida)
                    
                print(f"Extracción completada: {archivo} -> {carpeta_salida}")
                
            except zipfile.BadZipFile:
                print(f"Error: El archivo {archivo} está corrupto o no es válido.")
            except RuntimeError as e:
                if 'password' in str(e).lower():
                    print(f"Error: Contraseña incorrecta o el archivo {archivo} requiere una contraseña.")
                else:
                    print(f"Error inesperado en {archivo}: {e}")
            except Exception as e:
                print(f"Error inesperado en {archivo}: {e}")
    mover_archivos(carpeta_zip,'.zip')

def mover_archivos(carpeta_origen,  extension=None):
    """
    Mueve archivos desde una carpeta de origen a una carpeta de destino.
    Si se proporciona una extensión, solo se mueven los archivos con esa extensión.
    """
    # Generar el nombre de la subcarpeta con la fecha y hora actual
    fecha_actual = datetime.now().strftime("movido_%d-%m-%Y_%H-%M-%S")
    carpeta_destino = os.path.join(carpeta_origen, fecha_actual)
    
    # Verificar si la carpeta de destino existe, si no, crearla
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    # Recorrer todos los archivos en la carpeta de origen
    for archivo in os.listdir(carpeta_origen):
        ruta_origen = os.path.join(carpeta_origen, archivo)

        # Verificar si es un archivo (no una carpeta)
        if os.path.isfile(ruta_origen):
            # Si se especifica una extensión, mover solo los archivos con esa extensión
            if extension and not archivo.endswith(extension):
                continue

            ruta_destino = os.path.join(carpeta_destino, archivo)
            shutil.move(ruta_origen, ruta_destino)
            print(f"Movido: {archivo} -> {carpeta_destino}")

# # Ejemplo de uso
# zip_path = r'C:\Users\Gonzalo PL\Desktop\hyv\FEBRERO\17-02-25\INICIO\reguardo\17-02-25_08-39-06'
# output_dir = r'C:\Users\Gonzalo PL\Desktop\hyv\FEBRERO\17-02-25\INICIO\reguardo\17-02-25_08-39-06'
# password = ''  # Si no tiene contraseña, deja este valor como None

# descomprimir_todos_los_zip(zip_path, output_dir, password)