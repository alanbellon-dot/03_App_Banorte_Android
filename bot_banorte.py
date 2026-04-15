from appium import webdriver
from selenium.common.exceptions import TimeoutException
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
import time

class BotBanorte:
    def __init__(self, device_name):
        self.options = UiAutomator2Options()
        self.options.platform_name = 'Android'
        self.options.automation_name = 'UiAutomator2'
        self.options.device_name = device_name
        self.driver = None

    def conectar(self):
        self.driver = webdriver.Remote('http://127.0.0.1:4723', options=self.options)
        self.wait = WebDriverWait(self.driver, 15)
        print("¡Conectado al celular!")

    def scroll_hasta_abajo(self, repeticiones=2):
        print("Haciendo scroll hasta el fondo...")
        size = self.driver.get_window_size()
        start_y = int(size['height'] * 0.85) 
        end_y = int(size['height'] * 0.15)   
        start_x = int(size['width'] * 0.5)   

        for _ in range(repeticiones):
            actions = ActionBuilder(self.driver)
            pointer = actions.pointer_action
            pointer.move_to_location(start_x, start_y)
            pointer.pointer_down()
            pointer.move_to_location(start_x, end_y)
            pointer.pointer_up()
            actions.perform()
            time.sleep(1.5)

    def scroll_pequeno(self):
        """Hace un ligero deslizamiento para revelar el siguiente campo"""
        print("Acomodando pantalla (scroll)...")
        size = self.driver.get_window_size()
        start_y = int(size['height'] * 0.6) 
        end_y = int(size['height'] * 0.3) # Lo subimos un poquito más para asegurar que se vea   
        start_x = int(size['width'] * 0.5)

        actions = ActionBuilder(self.driver)
        pointer = actions.pointer_action
        pointer.move_to_location(start_x, start_y)
        pointer.pointer_down()
        pointer.move_to_location(start_x, end_y)
        pointer.pointer_up()
        actions.perform()
        time.sleep(1.5) # Le damos un respiro para que cargue la interfaz

    def firmar(self, xpath_caja_firma):
        print("Dibujando firma...")
        caja = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath_caja_firma)))
        rect = caja.rect
        
        start_x = rect['x'] + int(rect['width'] * 0.2)
        start_y = rect['y'] + int(rect['height'] * 0.5)
        end_x = rect['x'] + int(rect['width'] * 0.8)
        end_y = start_y

        actions = ActionBuilder(self.driver)
        pointer = actions.pointer_action
        pointer.move_to_location(start_x, start_y)
        pointer.pointer_down()
        pointer.move_to_location(end_x, end_y)
        pointer.pointer_up()
        actions.perform()
        time.sleep(1)

    def rutina_declaraciones(self):
        print("Iniciando Módulo Declaraciones...")
        
        # 1. Guardamos el tiempo original (15s) y lo cambiamos a 6s para este módulo
        wait_original = self.wait
        self.wait = WebDriverWait(self.driver, 6)
        
        try:
            self.scroll_hasta_abajo(repeticiones=2) 
            
            # Abrir Siniestro
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.mx.aseguradoradigital.banorte:id/fsiniestrosPRecycler"]/android.widget.FrameLayout[4]/androidx.appcompat.widget.LinearLayoutCompat/androidx.appcompat.widget.LinearLayoutCompat[1]/android.widget.RelativeLayout/androidx.appcompat.widget.LinearLayoutCompat'))).click()

            # Confirmar Arribo
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/farriboBtnConfirm"]'))).click()
            
            # --- ZONA: POP-UP DE ARRIBO ---
            print("Esperando pop-up de arribo (máximo 5 segundos)...")
            try:
                wait_corto = WebDriverWait(self.driver, 5)
                campo_serie = wait_corto.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[1]')))
                
                print("El pop-up apareció. Llenando datos...")
                campo_serie.clear()
                campo_serie.send_keys("111111")
                
                # Placa
                campo_placa = wait_corto.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[2]')))
                campo_placa.clear()
                campo_placa.send_keys("1111ZZZ")
                
                time.sleep(1) 
                
                # Checkbox "No coincide"
                wait_corto.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckBox[@resource-id="com.mx.aseguradoradigital.banorte:id/checkNoCoincide"]'))).click()
                
                time.sleep(1) 
                
                # Botón OK del pop-up
                wait_corto.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/dAlertInputBtnOk"]'))).click()
                
                time.sleep(2) 
            except TimeoutException:
                print("El pop-up de arribo no se mostró. Continuando con el flujo normal...")
            # ------------------------------------

            # Menú Captura
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//androidx.appcompat.widget.LinearLayoutCompat[@resource-id="com.mx.aseguradoradigital.banorte:id/menufBtnCaptura"]'))).click()
            
            # Declaraciones (Opción 1)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.mx.aseguradoradigital.banorte:id/capturaMenuFRecycler"]/android.widget.FrameLayout[1]/androidx.appcompat.widget.LinearLayoutCompat'))).click()
            
            # Escribir "Prueba"
            campo_prueba = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[1]')))
            campo_prueba.clear()
            campo_prueba.send_keys("Prueba")
            
            # Check Privacidad y Alert
            self.driver.find_element(AppiumBy.XPATH, '//android.widget.CheckBox[@resource-id="com.mx.aseguradoradigital.banorte:id/fDeclaraHechosCheckPrivacidad"]').click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/dAlertCommonBtnOk"]'))).click()
            
            # --- ZONA DE FORMULARIO CON SCROLLS ---
            self.scroll_pequeno()

            # Edad "30"
            campo_edad = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[4]')))
            campo_edad.clear()
            campo_edad.send_keys("30")
            
            self.scroll_pequeno()
            
            # Teléfono "555555"
            campo_tel = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[3]')))
            campo_tel.clear()
            campo_tel.send_keys("555555")
            
            self.scroll_pequeno()
            
            # Seleccionar Ciudad de México
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[1]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="Ciudad de México"]'))).click()
            
            # Seleccionar Permanente
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[2]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="Permanente"]'))).click()

            # Check Permanente
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckBox[@resource-id="com.mx.aseguradoradigital.banorte:id/fDeclaraCheckPermanente"]'))).click()
     
            # Firma 1 (Ajustador)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Button[@text="AÑADIR FIRMA DIGITAL"])[1]'))).click()
            self.firmar('//android.view.View[@resource-id="com.mx.aseguradoradigital.banorte:id/signaturePad"]')
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/signatureBtnOk"]'))).click()
      
            # Firma 2 (Conductor)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@text="AÑADIR FIRMA DIGITAL"]'))).click()
            self.firmar('//android.view.View[@resource-id="com.mx.aseguradoradigital.banorte:id/signaturePad"]')
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/signatureBtnOk"]'))).click()

            # Guardar Declaraciones
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/declaraBtnSave"]'))).click()
            
            # Pop-up final de confirmación
            print("Esperando pop-up de confirmación...")
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/dAlertCommonBtnOk"]'))).click()
            
            print("¡Módulo Declaraciones completado al 100%!")

        except Exception as e:
            # 2. Si el proceso falla o se traba (pasan 6 segs), cae automáticamente aquí
            print(f"\nEl proceso de Declaraciones no respondió o falló. Interrumpiendo módulo...")
            print("Apretando botón 'Navegar hacia arriba' para continuar con Asegurado...")
            try:
                # Usamos un wait cortito para apretar tu botón de regresar
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ImageButton[@content-desc="Navegar hacia arriba"]'))).click()
                time.sleep(2) # Pausa para dejar que la pantalla termine de regresar atrás
            except Exception as error_boton:
                print("No se pudo encontrar/apretar el botón de regresar.")
                
        finally:
            # 3. MUY IMPORTANTE: Antes de salir de esta función, restauramos el tiempo de espera a 15s
            # para que el siguiente módulo (Asegurado) funcione con el tiempo normal.
            self.wait = wait_original

    def rutina_asegurado(self):
        try:
            print("Iniciando Módulo Asegurado...")

            # 1. Ir DIRECTAMENTE a la opción 2 (Asegurado) porque ya estamos en el menú
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.mx.aseguradoradigital.banorte:id/capturaMenuFRecycler"]/android.widget.FrameLayout[2]/androidx.appcompat.widget.LinearLayoutCompat'))).click()

            # 2. Seleccionar Tratamiento
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckBox[@resource-id="com.mx.aseguradoradigital.banorte:id/vehiculoFCDPCheckTratamiento"]'))).click()

            # Pequeño scroll
            self.scroll_pequeno()

            # 3. Ubicación Tramo Ciudad
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[1]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="Ubicación Tramo Ciudad"]'))).click()

            # 4. Avenida
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[2]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="Avenida"]'))).click()

            # Pequeño scroll
            self.scroll_pequeno()

            # 5. Ciudad de México
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[1]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="CIUDAD DE MEXICO"]'))).click()

            # 6. Cuauhtémoc
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[2]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="Cuauhtémoc"]'))).click()

            # 7. Campo: Calle
            campo_calle = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[2]')))
            campo_calle.clear()
            campo_calle.send_keys("Calle")

            # 8. Campo: 10
            campo_diez = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[3]')))
            campo_diez.clear()
            campo_diez.send_keys("10")

            # 9. Campo: 1
            campo_uno = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[4]')))
            campo_uno.clear()
            campo_uno.send_keys("1")

            # 10. Campo: prueba
            campo_prueba = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[5]')))
            campo_prueba.clear()
            campo_prueba.send_keys("prueba")

            # Pequeño scroll hacia abajo
            self.scroll_pequeno()

            # 11. Añadir teléfono principal
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.TextView[@text="AÑADIR TELÉFONO"]'))).click()
            
            campo_tel_aseg = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"]')))
            campo_tel_aseg.clear()
            campo_tel_aseg.send_keys("5555555555")

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/dAlertInputBtnOk"]'))).click()

            # 12. Ocupantes (0)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.TextView[@text="OCUPANTES (0)"]'))).click()

            # 13. Autos SI
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.RadioButton[@resource-id="com.mx.aseguradoradigital.banorte:id/tercerosFACheckAutosSI"]'))).click()

            # 14. Nombre "ANA"
            campo_ana = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[1]')))
            campo_ana.clear()
            campo_ana.send_keys("ANA")

            # 15. "TEST" 1
            campo_test1 = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[2]')))
            campo_test1.clear()
            campo_test1.send_keys("TEST")

            # 16. "TEST" 2
            campo_test2 = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[3]')))
            campo_test2.clear()
            campo_test2.send_keys("TEST")

           # 17. Edad "30" (Usando el EditText en lugar del Layout)
            campo_edad_ocu = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[4]')))
            campo_edad_ocu.clear()
            campo_edad_ocu.send_keys("30")

            # 18. Check Tratamiento Ocupantes
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckBox[@resource-id="com.mx.aseguradoradigital.banorte:id/vehiculoOFDCCheckTratamiento"]'))).click()

            # 19. Lesiones SI
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.RadioButton[@resource-id="com.mx.aseguradoradigital.banorte:id/vehiculoOFDCCheckLesionesSI"]'))).click()

           # Pequeño scroll
            self.scroll_pequeno()

            # 20. Email 1 (Regresamos al índice [2] porque el scroll ocultó los de arriba)
            campo_email1 = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[2]')))
            campo_email1.clear()
            campo_email1.send_keys("PruebaBan@gmail.com")

            # 21. Email 2 (Regresamos al índice [3])
            campo_email2 = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[3]')))
            campo_email2.clear()
            campo_email2.send_keys("PruebaBan@gmail.com")

            # 22. Añadir Teléfono Ocupantes
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.TextView[@text="AÑADIR TELÉFONO"]'))).click()

            campo_tel_ocu = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"]')))
            campo_tel_ocu.clear()
            campo_tel_ocu.send_keys("1111111111")

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/dAlertInputBtnOk"]'))).click()

            # 23. Guardar Ocupante
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/vehiculoOContainerBtnSave"]'))).click()

            time.sleep(2) # <-- PAUSA VITAL: Esperar a que la app registre el guardado

           # 24. Seleccionar pestaña Conductor
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.LinearLayout[@content-desc="Conductor"]'))).click()

            time.sleep(2) # <-- PAUSA VITAL: Esperar a que termine la animación de cambio de pestaña

            # 25. Guardar Final Asegurado (Búsqueda Inteligente)
            print("Buscando botón de guardar Conductor...")
            try:
                # Intentamos buscarlo rápido (3 segundos) por si ya está visible
                wait_rapido = WebDriverWait(self.driver, 3)
                boton_guardar = wait_rapido.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/vehiculoCContainerBtnSave"]')))
                boton_guardar.click()
            except TimeoutException:
                # Si no lo encuentra en 3 segundos, hacemos un scroll seguro hacia abajo
                print("El botón no está a la vista. Deslizando hacia abajo...")
                self.scroll_hasta_abajo(repeticiones=1)
                
                # Y lo volvemos a buscar ya con el tiempo normal
                boton_guardar = self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/vehiculoCContainerBtnSave"]')))
                boton_guardar.click()
                # 26. Pop-up final de confirmación
            print("Esperando pop-up de confirmación final...")
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/dAlertCommonBtnOk"]'))).click()

            print("¡Módulo Asegurado completado al 100%!")

        except Exception as e:
            print(f"Error durante Asegurado: {e}")

    def cerrar_conexion(self):
        if self.driver:
            time.sleep(3)
            self.driver.quit()