from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import messagebox

def iniciar_sesion(driver, usuario, password, root):
    try:
        # Ingresar usuario
        user_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/div[2]/div[3]/div/div[3]/form/div[1]/div[1]/div[1]/div/div/input'))
        )
        user_input.send_keys(usuario)        

        # Ingresar contraseña
        pass_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/div[2]/div[3]/div/div[3]/form/div[1]/div[1]/div[2]/div/div/input'))
        )
        pass_input.send_keys(password)

        # Hacer clic en "Log in"
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div/div[2]/div[3]/div/div[3]/form/div[1]/div[2]/div/button'))
        ).click()
        # # Hacer clic en "Continue"
        # WebDriverWait(driver, 15).until(
        #     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/loginroute/div/logininit/div/div/securedpassword/div/div/div/form/div[3]/div/div/div[2]/oc-action-button/button'))
        # ).click()

        # # Solicitar código de verificación
        # messagebox.showinfo("[Automatización Descarga Citibank]", "Ingrese el código de verificación por favor.", parent=root)

        # # Esperar a que el botón de inicio de sesión esté disponible y hacer clic
        # WebDriverWait(driver, 120).until(
        #     EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/loginroute/div/logininit/div/div/gmt/div[2]/div/div/form/div/div/div[2]/div[3]/oc-action-button/button'))
        # ).click()

        # print("*** Credenciales y código de verificación ingresados correctamente ***")

        # # Eliminar overlay si existe
        # try:
        #     WebDriverWait(driver, 15).until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR, ".cps-portal-backdrop"))
        #     )
        #     driver.execute_script("""
        #         let overlay = document.querySelector('.cps-portal-backdrop'); 
        #         if (overlay) { overlay.parentNode.removeChild(overlay); }
        #     """)
        #     print("Overlay eliminado.")

        #     # Clic en botón OK del modal si aparece
        #     boton_ok = WebDriverWait(driver, 25).until(
        #         EC.element_to_be_clickable((By.XPATH, "//button[text()='OK']"))
        #     )
        #     boton_ok.click()
        #     print("Botón OK clickeado con éxito.")

        # except Exception as e:
        #     print(f"Error al interactuar con el modal: {e}")

    except:
        messagebox.showerror("[Automatización Descarga Citibank]", "¡ERROR! No se pudo ingresar las credenciales", parent=root)
        raise
