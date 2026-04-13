from appium import webdriver
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
        try:
            self.scroll_hasta_abajo(repeticiones=2) 
            
            # 1. Abrir Siniestro
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.mx.aseguradoradigital.banorte:id/fsiniestrosPRecycler"]/android.widget.FrameLayout[4]/androidx.appcompat.widget.LinearLayoutCompat/androidx.appcompat.widget.LinearLayoutCompat[1]/android.widget.RelativeLayout/androidx.appcompat.widget.LinearLayoutCompat'))).click()

            # 2. Confirmar Arribo
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/farriboBtnConfirm"]'))).click()
            
            # --- NUEVA ZONA: POP-UP DE ARRIBO ---
            print("Llenando datos del pop-up de arribo...")
            
            # Serie
            campo_serie = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[1]')))
            campo_serie.clear()
            campo_serie.send_keys("111111")
            
            # Placa
            campo_placa = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[2]')))
            campo_placa.clear()
            campo_placa.send_keys("1111ZZZ")
            
            # Checkbox "No coincide"
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckBox[@resource-id="com.mx.aseguradoradigital.banorte:id/checkNoCoincide"]'))).click()
            
            # Botón OK del pop-up
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/dAlertInputBtnOk"]'))).click()
            # ------------------------------------

            # 3. Menú Captura
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//androidx.appcompat.widget.LinearLayoutCompat[@resource-id="com.mx.aseguradoradigital.banorte:id/menufBtnCaptura"]'))).click()
            
            # 4. Declaraciones (Opción 1)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.mx.aseguradoradigital.banorte:id/capturaMenuFRecycler"]/android.widget.FrameLayout[1]/androidx.appcompat.widget.LinearLayoutCompat'))).click()
            
            # 5. Escribir "Prueba" (Usamos clear por si acaso)
            campo_prueba = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[1]')))
            campo_prueba.clear()
            campo_prueba.send_keys("Prueba")
            
            # 6. Check Privacidad y Alert
            self.driver.find_element(AppiumBy.XPATH, '//android.widget.CheckBox[@resource-id="com.mx.aseguradoradigital.banorte:id/fDeclaraHechosCheckPrivacidad"]').click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/dAlertCommonBtnOk"]'))).click()
            
            # --- ZONA DE FORMULARIO CON SCROLLS ---
            self.scroll_pequeno()

            # 7. Edad "30" (Actualizado al XPath correcto [4])
            campo_edad = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[4]')))
            campo_edad.clear()
            campo_edad.send_keys("30")
            
            self.scroll_pequeno()
            
            # 8. Teléfono "555555" (Usando tu nuevo XPath index [3])
            campo_tel = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[3]')))
            campo_tel.clear()
            campo_tel.send_keys("555555")
            
            self.scroll_pequeno()
            
            # 9. Seleccionar Ciudad de México
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[1]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="Ciudad de México"]'))).click()
            
            # 10. Seleccionar Permanente
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[2]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="Permanente"]'))).click()

            # 11. Check Permanente
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckBox[@resource-id="com.mx.aseguradoradigital.banorte:id/fDeclaraCheckPermanente"]'))).click()
     
            # 12. Firma 1 (Ajustador)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Button[@text="AÑADIR FIRMA DIGITAL"])[1]'))).click()
            self.firmar('//android.view.View[@resource-id="com.mx.aseguradoradigital.banorte:id/signaturePad"]')
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/signatureBtnOk"]'))).click()
      
            # 13. Firma 2 (Conductor)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@text="AÑADIR FIRMA DIGITAL"]'))).click()
            self.firmar('//android.view.View[@resource-id="com.mx.aseguradoradigital.banorte:id/signaturePad"]')
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/signatureBtnOk"]'))).click()

            # 14. Guardar Declaraciones
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/declaraBtnSave"]'))).click()
            
            # 15. Pop-up final de confirmación (Sin scroll)
            print("Esperando pop-up de confirmación...")
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/dAlertCommonBtnOk"]'))).click()
            
            print("¡Módulo Declaraciones completado al 100%!")

        except Exception as e:
            print(f"Error durante Declaraciones: {e}")

    def cerrar_conexion(self):
        if self.driver:
            time.sleep(3)
            self.driver.quit()