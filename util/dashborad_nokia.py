from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
def dashboard(driver,download_folder):
    try:
        elemento = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'inventory/')]"))
        )
        print("El elemento es clickeable.")
        elemento.click()
        
        elemento_select = WebDriverWait(driver,15).until(
            EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/md-content/div/md-content/div/ng-include/md-sidenav/div/epg-filter-management/div/div[2]/div/div/md-input-container/md-select"))
        )
        elemento_select.click()
        
        elemento_select_jmeza = WebDriverWait(driver,15).until(
            EC.element_to_be_clickable((By.XPATH,"/html/body/div[4]/md-select-menu/md-content/md-option[2]"))
        )
        elemento_select_jmeza.click()
        
        elemento_select_query = WebDriverWait(driver,15).until(
            EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/md-content/div/md-content/div/ng-include/md-sidenav/div/md-content/form/div/button"))
        )
        elemento_select_query.click()
        
        while True:
            try:
                elemento_select_save = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/md-content/div/md-content/div/div[2]/collected-inventory-view/md-card/md-card-title/div[2]/export-csv-file"))
                )
                elemento_select_save.click()
                print("Botón encontrado y clickeado")
                break  # Sale del bucle cuando el botón aparece y se hace clic
            except TimeoutException:
                print("Esperando que aparezca el botón...")
        
        
        
        
        ultimo_progreso = -1  # Inicializamos con un valor que no será alcanzado
        progeso_completado = 0
        # Esperar hasta que el progreso llegue al 100%+
        while True:
            try:
                progress_element = driver.find_element(By.XPATH, "//span[contains(text(), '% completed')]")
                progress_text = progress_element.text.split('%')[0].strip()
                progress = int(progress_text)

                if progress != ultimo_progreso:  # Solo imprimimos si cambia el porcentaje
                    print(f"Progreso actual: {progress}%")
                    ultimo_progreso = progress  # Actualizamos el último progreso mostrado
                
                if progress >= 100:
                    print("Proceso completado.")
                    # Espera a que el botón "SHOW DETAILS" sea clickeable y hace clic
                    progeso_completado = progress
                    break

            except Exception as e:
                print("Esperando progreso...")

            time.sleep(10)  # Esperar 10 segundos antes de verificar nuevamente
        
        if progeso_completado >= 100:
            boton_detalles = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@auto-id='showDetailsButton']"))
            )
            boton_detalles.click()
            print(driver.current_url)  # Verifica si cambió la URL
            # Esperar a que se abra la nueva pestaña
            WebDriverWait(driver, 5).until(lambda d: len(d.window_handles) > 1)

            # Cambiar a la nueva pestaña
            driver.switch_to.window(driver.window_handles[1])
            print("Nueva URL:", driver.current_url)  # Ahora imprimirá la URL correcta
            
            
            elemento_descarga = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'here')]"))
            )
            print("El elemento es clickeable.")
            elemento_descarga.click()
            # Esperar a que desaparezca el archivo temporal de descarga
            while any(filename.endswith((".crdownload", ".part",".tmp")) for filename in os.listdir(download_folder)):
                print("Descarga en progreso...")
                time.sleep(5)

            print("Descarga completada.")

            # Cerrar el navegador
            driver.quit()
        else:
            print(f'tenemos un problema con el progreso : {progeso_completado}')
        
    except Exception as e:
        print(f"Error al hacer clic: {e}")