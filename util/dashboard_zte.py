from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os

def dashboard_zte(driver,download_folder,valores_formato):
    try:
        driver.refresh()
        time.sleep(3)
        
        # Verificar si el `iframe` principal está en el DOM
        try:
            iframe = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "page-mainIframe"))
            )
            print("Iframe encontrado en el DOM.")
        except:
            print("ERROR: Iframe NO encontrado.")

        driver.switch_to.frame(iframe)  # Cambiar al iframe principal
        print("Cambiado correctamente a IFRAME")
        
        query_button = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Query Conditions')]"))
        )

        # Esperar hasta que el botón sea visible y clickeable
        query_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Query Conditions')]"))
        )

        print("✅ Botón encontrado, haciendo clic...")
        query_button.click()
        
        # Ingresar usuario
        
        for index, item in enumerate(valores_formato):
            print(f'buscaresmo a {item}')
            user_input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/app-root/res-query/onu-optical-module-query/div/onu-optical-module-query-condition/plx-form/form/div/div[1]/div[1]/div/div[2]/div/div[1]/an-groups-nes-picker/div/plx-picklist/div/div[1]/div[2]/div/div/plx-search/div/div/plx-input-ellipsis-container/input'))
            )
            user_input.clear()
            user_input.send_keys(item)
            
            query_button_filtro = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/app-root/res-query/onu-optical-module-query/div/onu-optical-module-query-condition/plx-form/form/div/div[1]/div[1]/div/div[2]/div/div[1]/an-groups-nes-picker/div/plx-picklist/div/div[1]/div[2]/div/div/plx-search/div/li"))
            )
            query_button_filtro.click()
            print('esperamos 3 segundos')
            time.sleep(3)
               
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//ul[contains(@class, 'plx-treenode-children')]"))
            )

            # Obtener y mostrar los nombres de los nodos encontrados antes de seleccionarlos
            tree_nodes = driver.find_elements(By.XPATH, "//ul[contains(@class, 'plx-treenode-children')]//li[@class='plx-treenode']")

            if not tree_nodes:
                print("❌ No se encontraron nodos para seleccionar.")
            else:
                print(f"✅ Se encontraron {len(tree_nodes)} elementos `plx-tree-node`.")
                
                # Imprimir los nombres de los nodos antes de seleccionarlos
                for index, node in enumerate(tree_nodes):
                    try:
                        label = node.find_element(By.XPATH, ".//span[contains(@class, 'plx-treenode-lable-span')]")
                        print(f"🔹 Nodo {index + 1}: {label.text}")
                    except:
                        print(f"⚠️ No se pudo obtener el nombre del nodo en el índice {index}")

            # Seleccionar y pasar cada nodo uno por uno
            for index in range(1, len(tree_nodes)):
                try:
                    # Volver a obtener los nodos en cada iteración para evitar `stale element`
                    tree_nodes = driver.find_elements(By.XPATH, "//ul[contains(@class, 'plx-treenode-children')]//li[@class='plx-treenode']")
                    node = tree_nodes[index]

                    # Buscar el `span` dentro del nodo para hacer clic
                    label = node.find_element(By.XPATH, ".//span[contains(@class, 'plx-treenode-lable-span')]")

                    # Hacer scroll hasta el elemento para asegurarnos de que es visible
                    driver.execute_script("arguments[0].scrollIntoView();", label)

                    # Hacer clic en el nodo
                    label.click()
                    print(f"✅ Nodo seleccionado: {label.text}")

                    time.sleep(0.5)  # Pequeña pausa para evitar problemas

                    # Esperar que el botón de flecha derecha sea clickeable
                    arrow_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'plx-picklist-transfer-btn plx-ico-arrow-right-16')]"))
                    )

                    # Hacer clic en la flecha para mover el nodo seleccionado
                    arrow_button.click()
                    print(f"➡ Nodo movido: {label.text}")

                    time.sleep(1)  # Pequeña pausa para evitar errores de renderizado
                    
                except Exception as e:
                    print(f"❌ Error al seleccionar un nodo en el índice {index}: {e}")
        print('Esperamos 3 segundos para dar click a OK')
        time.sleep(3)
        
        # Esperar hasta que el botón sea visible y clickeable
        query_button_OK = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]"))
        )

        print("✅ Botón OK, haciendo clic...")
        query_button_OK.click()
        
        print('Esperamos hasta que termien de cargars el datatable')
        time.sleep(5)
        print('damos click al boton Export All')
        botton_export_all =WebDriverWait(driver,15).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/res-query/onu-optical-module-query/div/onu-optical-module-query-result/an-res-query-stats-result/plx-table/div/div/div[1]/div[2]/div[2]/div/button'))
        )
        botton_export_all.click()
        print('damos click al boton excel')
        time.sleep(1)
        botton_excel =WebDriverWait(driver,15).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/res-query/onu-optical-module-query/div/onu-optical-module-query-result/an-res-query-stats-result/plx-table/div/div/div[1]/div[2]/div[2]/div/div/button[2]'))
        )
        botton_excel.click()

        print('Regresamos al iframe principal')
        driver.switch_to.default_content()
        time.sleep(1)       
         
        print('Damos click al botón Export Record')  
        boton_export_record = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/ptl-framework/div/div[1]/ptl-side-menu/div/div/div/ul/li[15]/div/span"))
        )

        boton_export_record.click()
        print("✅ Click en Export Record exitoso.")
        
        
        time.sleep(5)
        
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"🔍 Se encontraron {len(iframes)} iframes en la página.")

        for index, iframe in enumerate(iframes):
            print(f"🔹 IFRAME {index}: {iframe.get_attribute('name')} | ID: {iframe.get_attribute('id')}")
            
        # Verificar si el `iframe` principal está en el DOM
        try:
            iframe = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "page-mainIframe"))
            )
            print("Iframe encontrado en el DOM.")
        except:
            print("ERROR: Iframe NO encontrado.")

        driver.switch_to.frame(iframe)  # Cambiar al iframe principal
        print("Cambiado correctamente a IFRAME")
        print("Ingresamos a la tabla y selecionamos rl t-body")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tbody"))
        )

        # Esperar hasta que el estado cambie a "Succeeded"
        estado = "In Progress"
        while estado == "In Progress":
            try:
                driver.refresh()
                time.sleep(2)
                try:
                    iframe = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.ID, "page-mainIframe"))
                    )
                    print("Iframe encontrado en el DOM.")
                except:
                    print("ERROR: Iframe NO encontrado.")

                driver.switch_to.frame(iframe)
                # Encontrar el estado en la primera fila de la tabla
                estado_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//tbody/tr[1]/td[8]/span"))  # Columna del estado
                )
                estado = estado_element.text.strip()
                print(f"🔄 Estado actual: {estado}")

                # Si el estado aún es "In Progress", refrescar la página y esperar antes de verificar nuevamente
                if estado == "In Progress":
                    driver.refresh()
                    time.sleep(2)  # Esperar antes de volver a verificar
                elif estado == 'Succeeded':
                    estado == 'Succeeded'
            except Exception as e:
                print(f"⚠️ Error al obtener el estado: {e}")
                driver.refresh()
                time.sleep(5)  # Esperar antes de volver a intentar

        if estado == 'Succeeded':
            print("✅ Estado cambiado a 'Succeeded'. Procediendo con la descarga...")
            # Encontrar el botón "Download" de la primera fila
            download_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//tbody/tr[1]//button[contains(text(), 'Download')]"))
            )
            # Hacer clic en el botón de Download
            download_button.click()
            time.sleep(10)
            driver.quit()
            print("Descarga completada.")
        else:
            print("X validaremos")
            
    except Exception as e:
        print("⚠️ Error:", str(e))