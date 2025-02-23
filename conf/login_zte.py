from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import messagebox
import time
def iniciar_sesion_zte(driver, usuario, password):
    try:
        # Ingresar usuario
        user_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[2]/div[1]/div[4]/input'))
        )
        user_input.send_keys(usuario)        

        # Ingresar contraseña
        pass_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[2]/div[1]/div[5]/input[2]'))
        )
        pass_input.send_keys(password)

        # Hacer clic en "Log in"
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[2]/button'))
        ).click()
        
        time.sleep(3)
        # Cambiar la URL a la nueva página deseada
        nueva_url = "https://10.125.60.3:28001/an-portal/framework/default.html#/_onu-optical-module-resource-query"
        driver.get(nueva_url)
    except Exception as e:
        print("⚠️ Error:", str(e))
