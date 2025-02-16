import openpyxl
import tkinter as tk
from tkinter import messagebox
import sys
import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conf.login import iniciar_sesion
from conf.login_zte import iniciar_sesion_zte
from util.dashborad import dashboard
from util.dashboard_zte import dashboard_zte
import os
import datetime

# Configuración inicial
root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True)

try:
    wbconf = openpyxl.load_workbook('conf/conf.xlsx')
    hojaconf = wbconf['Hoja1']
    usuario = hojaconf['C3'].value
    password = hojaconf['C4'].value
    password_zte = hojaconf['C6'].value
    # fecha_desde_excel = hojaconf['C6'].value
    # fecha_hasta_excel = hojaconf['C7'].value
    rutaDescarga = hojaconf['C5'].value
    
    # Leer toda la columna F desde la fila 3 en adelante (asumiendo que los datos empiezan ahí)
    # Leer toda la columna F desde la fila 3 en adelante
    valores_f = set()
    for cell in hojaconf['F']:
        if cell.value:  # Filtrar solo valores no vacíos
            valores_f.add(cell.value)

    print(f'usuario_nokia:  {usuario}\npassword_nokia: {password}\npassword_zte:  {password_zte}\nOlt_Descargar: {valores_f}')
    
except:
    messagebox.showerror("Error", "¡ERROR! Cierra el archivo de configuración")
    sys.exit()


# # fecha_actual = datetime.datetime.now()
# # fecha_actual = datetime.datetime(2025, 2, 14, 16, 0, 0)
fecha_actual = datetime.datetime.now()
formato_fecha = fecha_actual.strftime("%d-%m-%y")
hora_actual = fecha_actual.strftime("%H-%M-%S")  # Para reguardo

ruta_fecha = os.path.join(rutaDescarga, formato_fecha)
hora_del_dia = fecha_actual.hour
if hora_del_dia < 15:  # Antes de las 6:00 PM se guarda en "inicio"
    periodo = "INICIO"
else:  # A partir de las 6:00 PM se guarda en "final"
    periodo = "FINAL"
    
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


#Instalar automaticamente la vesion compatible del chrmedriver
chromedriver_autoinstaller.install()
prefs = {
    "download.default_directory": ruta_final #Guargar en la ruta especificada
}
#Opciones de chrome 
def iniciar_navegador():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--headless=new')  # Ejecutar en modo headless (sin interfaz gráfica)
    chrome_options.add_argument('--mute-audio')  # Silenciar el audio del navegador
    chrome_options.add_experimental_option("detach", True)  # Evita que Chrome se cierre al finalizar el script
    return webdriver.Chrome(options=chrome_options)


driver = iniciar_navegador()
driver.get('https://10.125.60.3:28001/api/oauth2/v1/authorize?scope=user.login&response_type=code&redirect_uri=/an-portal/framework/default.html') 
iniciar_sesion_zte(driver, usuario, password_zte, root)
dashboard_zte(driver,ruta_final,valores_f)

print('esperamos 5 segundo para que abrir la otra nevagacion')
time.sleep(5)

# #NOKIA
driver = iniciar_navegador()
driver.get('https://10.252.203.66:32443/nokia-altiplano-ac/intents/login.html#/app/browser/intentTypes')
iniciar_sesion(driver, usuario, password, root)
dashboard(driver,ruta_final)






