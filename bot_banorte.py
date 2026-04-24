from appium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException 
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
        size = self.driver.get_window_size()
        start_y = int(size['height'] * 0.6) 
        end_y = int(size['height'] * 0.3) 
        start_x = int(size['width'] * 0.5)

        actions = ActionBuilder(self.driver)
        pointer = actions.pointer_action
        pointer.move_to_location(start_x, start_y)
        pointer.pointer_down()
        pointer.move_to_location(start_x, end_y)
        pointer.pointer_up()
        actions.perform()
        time.sleep(1.5)

    def scroll_muy_pequeno(self):
        size = self.driver.get_window_size()
        start_y = int(size['height'] * 0.5) 
        # Cambiamos de 0.4 a 0.35 para que haga un poco más de recorrido
        end_y = int(size['height'] * 0.35)   
        start_x = int(size['width'] * 0.5)

        actions = ActionBuilder(self.driver)
        pointer = actions.pointer_action
        pointer.move_to_location(start_x, start_y)
        pointer.pointer_down()
        pointer.move_to_location(start_x, end_y)
        pointer.pointer_up()
        actions.perform()
        time.sleep(1.5)

    def scroll_horizontal(self):
        print("Haciendo scroll horizontal en los iconos...")
        size = self.driver.get_window_size()
        start_y = int(size['height'] * 0.78) 
        start_x = int(size['width'] * 0.8) 
        end_x = int(size['width'] * 0.1)   

        actions = ActionBuilder(self.driver)
        pointer = actions.pointer_action
        pointer.move_to_location(start_x, start_y)
        pointer.pointer_down()
        pointer.pause(1.0) 
        pointer.move_to_location(end_x, start_y)
        pointer.pointer_up()
        actions.perform()
        time.sleep(1.5)

    def mover_icono_ya_en_pantalla(self, xpath_icono, offset_x=0, offset_y=0):
        icono = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath_icono)))
        mapa = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.ImageView[@resource-id="com.mx.aseguradoradigital.banorte:id/ivmap"]')))

        mapa_rect = mapa.rect
        centro_mapa_x = mapa_rect['x'] + int(mapa_rect['width'] * 0.5) + offset_x
        centro_mapa_y = mapa_rect['y'] + int(mapa_rect['height'] * 0.5) + offset_y

        icono_rect = icono.rect
        centro_icono_x = icono_rect['x'] + int(icono_rect['width'] * 0.5)
        centro_icono_y = icono_rect['y'] + int(icono_rect['height'] * 0.5)

        actions = ActionBuilder(self.driver)
        pointer = actions.pointer_action
        pointer.move_to_location(centro_icono_x, centro_icono_y)
        pointer.pointer_down()
        pointer.pause(1.0) 
        pointer.move_to_location(centro_mapa_x, centro_mapa_y)
        pointer.pointer_up()
        actions.perform()
        time.sleep(1)

    def girar_elemento_derecha(self, xpath_elemento):
        print("Girando icono hacia el este...")
        elemento = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, xpath_elemento)))
        rect = elemento.rect
        centro_x = rect['x'] + int(rect['width'] * 0.5)
        centro_y = rect['y'] + int(rect['height'] * 0.5)

        start_x = centro_x
        start_y = centro_y - int(rect['height'] * 0.4) 
        end_x = centro_x + int(rect['width'] * 0.8)    
        end_y = centro_y

        actions = ActionBuilder(self.driver)
        pointer = actions.pointer_action
        pointer.move_to_location(start_x, start_y)
        pointer.pointer_down()
        pointer.pause(1.5) 
        pointer.move_to_location(end_x, end_y)
        pointer.pointer_up()
        actions.perform()
        time.sleep(1)

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
        try:
            self.scroll_hasta_abajo(repeticiones=2) 
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.mx.aseguradoradigital.banorte:id/fsiniestrosPRecycler"]/android.widget.FrameLayout[4]/androidx.appcompat.widget.LinearLayoutCompat/androidx.appcompat.widget.LinearLayoutCompat[1]/android.widget.RelativeLayout/androidx.appcompat.widget.LinearLayoutCompat'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/farriboBtnConfirm"]'))).click()
            
            print("Esperando pop-up de arribo (máximo 5 segundos)...")
            try:
                wait_corto = WebDriverWait(self.driver, 5)
                campo_serie = wait_corto.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[1]')))
                campo_serie.clear()
                campo_serie.send_keys("111111")
                campo_placa = wait_corto.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[2]')))
                campo_placa.clear()
                campo_placa.send_keys("1111ZZZ")
                time.sleep(1) 
                wait_corto.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckBox[@resource-id="com.mx.aseguradoradigital.banorte:id/checkNoCoincide"]'))).click()
                time.sleep(1) 
                wait_corto.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/dAlertInputBtnOk"]'))).click()
                time.sleep(2) 
            except TimeoutException:
                print("El pop-up de arribo no se mostró. Continuando con el flujo normal...")

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//androidx.appcompat.widget.LinearLayoutCompat[@resource-id="com.mx.aseguradoradigital.banorte:id/menufBtnCaptura"]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.mx.aseguradoradigital.banorte:id/capturaMenuFRecycler"]/android.widget.FrameLayout[1]/androidx.appcompat.widget.LinearLayoutCompat'))).click()
            
        except Exception as e:
            print("No se pudo iniciar/abrir el módulo de Declaraciones. Saltando módulo...")
            return 
            
        wait_original = self.wait
        self.wait = WebDriverWait(self.driver, 6)
        
        try:
            campo_prueba = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[1]')))
            campo_prueba.clear()
            campo_prueba.send_keys("Prueba")
            
            self.driver.find_element(AppiumBy.XPATH, '//android.widget.CheckBox[@resource-id="com.mx.aseguradoradigital.banorte:id/fDeclaraHechosCheckPrivacidad"]').click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/dAlertCommonBtnOk"]'))).click()
            
            self.scroll_pequeno()

            campo_edad = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[4]')))
            campo_edad.clear()
            campo_edad.send_keys("30")
            
            self.scroll_pequeno()
            
            campo_tel = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[3]')))
            campo_tel.clear()
            campo_tel.send_keys("555555")
            
            self.scroll_pequeno()
            
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[1]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="Ciudad de México"]'))).click()
            
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[2]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="Permanente"]'))).click()

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckBox[@resource-id="com.mx.aseguradoradigital.banorte:id/fDeclaraCheckPermanente"]'))).click()
     
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Button[@text="AÑADIR FIRMA DIGITAL"])[1]'))).click()
            self.firmar('//android.view.View[@resource-id="com.mx.aseguradoradigital.banorte:id/signaturePad"]')
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/signatureBtnOk"]'))).click()
      
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@text="AÑADIR FIRMA DIGITAL"]'))).click()
            self.firmar('//android.view.View[@resource-id="com.mx.aseguradoradigital.banorte:id/signaturePad"]')
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/signatureBtnOk"]'))).click()

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/declaraBtnSave"]'))).click()
            
            print("Esperando pop-up de confirmación...")
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/dAlertCommonBtnOk"]'))).click()
            
            print("¡Módulo Declaraciones completado al 100%!")

        except Exception as e:
            print(f"\nEl proceso de Declaraciones no respondió o falló. Interrumpiendo módulo...")
            try:
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ImageButton[@content-desc="Navegar hacia arriba"]'))).click()
                time.sleep(2) 
            except Exception as error_boton:
                pass
                
        finally:
            self.wait = wait_original

    def rutina_asegurado(self):
        print("Iniciando Módulo Asegurado...")
        try:
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.mx.aseguradoradigital.banorte:id/capturaMenuFRecycler"]/android.widget.FrameLayout[2]/androidx.appcompat.widget.LinearLayoutCompat'))).click()
        except Exception as e:
            print("No se pudo entrar a la Opción 2. Saltando módulo...")
            return
            
        wait_original = self.wait
        self.wait = WebDriverWait(self.driver, 6)
        
        try:
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckBox[@resource-id="com.mx.aseguradoradigital.banorte:id/vehiculoFCDPCheckTratamiento"]'))).click()
            self.scroll_pequeno()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[1]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="Ubicación Tramo Ciudad"]'))).click()

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[2]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="Avenida"]'))).click()
            self.scroll_pequeno()

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[1]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="CIUDAD DE MEXICO"]'))).click()

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[2]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="Cuauhtémoc"]'))).click()

            campo_calle = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[2]')))
            campo_calle.clear()
            campo_calle.send_keys("Calle")

            campo_diez = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[3]')))
            campo_diez.clear()
            campo_diez.send_keys("10")

            campo_uno = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[4]')))
            campo_uno.clear()
            campo_uno.send_keys("1")

            campo_prueba = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[5]')))
            campo_prueba.clear()
            campo_prueba.send_keys("prueba")
            self.scroll_pequeno()

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.TextView[@text="AÑADIR TELÉFONO"]'))).click()
            
            campo_tel_aseg = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"]')))
            campo_tel_aseg.clear()
            campo_tel_aseg.send_keys("5555555555")

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/dAlertInputBtnOk"]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.TextView[@text="OCUPANTES (0)"]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.RadioButton[@resource-id="com.mx.aseguradoradigital.banorte:id/tercerosFACheckAutosSI"]'))).click()

            campo_ana = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[1]')))
            campo_ana.clear()
            campo_ana.send_keys("ANA")

            campo_test1 = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[2]')))
            campo_test1.clear()
            campo_test1.send_keys("TEST")

            campo_test2 = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[3]')))
            campo_test2.clear()
            campo_test2.send_keys("TEST")

            campo_edad_ocu = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[4]')))
            campo_edad_ocu.clear()
            campo_edad_ocu.send_keys("30")

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckBox[@resource-id="com.mx.aseguradoradigital.banorte:id/vehiculoOFDCCheckTratamiento"]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.RadioButton[@resource-id="com.mx.aseguradoradigital.banorte:id/vehiculoOFDCCheckLesionesSI"]'))).click()
            self.scroll_pequeno()

            campo_email1 = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[2]')))
            campo_email1.clear()
            campo_email1.send_keys("PruebaBan@gmail.com")

            campo_email2 = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[3]')))
            campo_email2.clear()
            campo_email2.send_keys("PruebaBan@gmail.com")

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.TextView[@text="AÑADIR TELÉFONO"]'))).click()

            campo_tel_ocu = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"]')))
            campo_tel_ocu.clear()
            campo_tel_ocu.send_keys("1111111111")

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/dAlertInputBtnOk"]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/vehiculoOContainerBtnSave"]'))).click()
            time.sleep(2) 

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.LinearLayout[@content-desc="Conductor"]'))).click()
            time.sleep(2) 

            try:
                wait_rapido = WebDriverWait(self.driver, 3)
                boton_guardar = wait_rapido.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/vehiculoCContainerBtnSave"]')))
                boton_guardar.click()
            except TimeoutException:
                self.scroll_hasta_abajo(repeticiones=1)
                boton_guardar = self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/vehiculoCContainerBtnSave"]')))
                boton_guardar.click()

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/dAlertCommonBtnOk"]'))).click()

            print("¡Módulo Asegurado completado al 100%!")

        except Exception as e:
            print(f"\nEl proceso de Asegurado no respondió o falló. Interrumpiendo módulo...")
            try:
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ImageButton[@content-desc="Navegar hacia arriba"]'))).click()
                time.sleep(2) 
            except Exception as error_boton:
                pass
                
        finally:
            self.wait = wait_original

    def rutina_deslinde(self):
        print("Iniciando Módulo Deslinde de Responsabilidad...")
        try:
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.mx.aseguradoradigital.banorte:id/capturaMenuFRecycler"]/android.widget.FrameLayout[3]/androidx.appcompat.widget.LinearLayoutCompat'))).click()
            time.sleep(2) 
        except Exception as e:
            print("No se pudo entrar a la Opción 3. Saltando módulo...")
            return 

        wait_original = self.wait
        self.wait = WebDriverWait(self.driver, 10) 
        
        try:
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[1]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="Me incorporaba"]'))).click()

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[2]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="Cambiaba de carril"]'))).click()

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/ccircunstanciaBtnEstablish"]'))).click()
            time.sleep(1)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/ccircunstanciaBtnEstablish"]'))).click()
            
            time.sleep(3) 
            
            print("Seleccionando y acomodando vehículo 1...")
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.ImageView[@resource-id="com.mx.aseguradoradigital.banorte:id/itemStickerImg"])[3]'))).click()
            time.sleep(1)
            
            xpath_coche1 = '//android.widget.RelativeLayout[@resource-id="com.mx.aseguradoradigital.banorte:id/ccircunstanciaCITemsRecreation"]/android.widget.ImageView[2]'
            self.mover_icono_ya_en_pantalla(xpath_coche1, offset_x=0, offset_y=0)
            self.girar_elemento_derecha(xpath_coche1)
            
            print("Seleccionando y acomodando vehículo 2...")
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.ImageView[@resource-id="com.mx.aseguradoradigital.banorte:id/itemStickerImg"])[4]'))).click()
            time.sleep(1)
            
            xpath_coche2 = '//android.widget.RelativeLayout[@resource-id="com.mx.aseguradoradigital.banorte:id/ccircunstanciaCITemsRecreation"]/android.widget.ImageView[3]'
            self.mover_icono_ya_en_pantalla(xpath_coche2, offset_x=100, offset_y=0)
            
            self.scroll_horizontal()
            print("Seleccionando y acomodando impacto (Boom)...")
            
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.ImageView[@resource-id="com.mx.aseguradoradigital.banorte:id/itemStickerImg"])[7]'))).click()
            time.sleep(1)
            
            xpath_boom = '//android.widget.RelativeLayout[@resource-id="com.mx.aseguradoradigital.banorte:id/ccircunstanciaCITemsRecreation"]/android.widget.ImageView[4]'
            self.mover_icono_ya_en_pantalla(xpath_boom, offset_x=50, offset_y=0)
            
            print("Buscando botón para firmar...")
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/ccircunstanciaBtnFirma"]'))).click()
            
            self.firmar('//android.view.View[@resource-id="com.mx.aseguradoradigital.banorte:id/signaturePad"]')
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/signatureBtnOk"]'))).click()
            
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@text="ESTABLECER"]'))).click()
            
            print("Esperando pop-up de confirmación final...")
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/dAlertCommonBtnOk"]'))).click()

            print("¡Módulo Deslinde completado al 100%!")

        except Exception as e:
            print(f"\nEl proceso de Deslinde no respondió o falló. Interrumpiendo módulo...")
            try:
                # Primera vez que regresa
                boton_atras = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ImageButton[@content-desc="Navegar hacia arriba"]')))
                boton_atras.click()
                time.sleep(1.5)
                # Segunda vez que regresa
                boton_atras = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ImageButton[@content-desc="Navegar hacia arriba"]')))
                boton_atras.click()
                time.sleep(2)
            except Exception:
                pass
                
        finally:
            self.wait = wait_original

    def rutina_terceros(self):
        print("Iniciando Módulo Terceros...")
        try:
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.mx.aseguradoradigital.banorte:id/capturaMenuFRecycler"]/android.widget.FrameLayout[6]/androidx.appcompat.widget.LinearLayoutCompat'))).click()
        except Exception as e:
            print("No se pudo entrar al módulo de Terceros. Saltando...")
            return

        wait_original = self.wait
        self.wait = WebDriverWait(self.driver, 8)

        try:
            # ==============================
            # PESTAÑA 1: CONDUCTOR (TERCERO)
            # ==============================
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.RadioButton[@resource-id="com.mx.aseguradoradigital.banorte:id/tercerosFACheckAutosSI"]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//androidx.appcompat.widget.LinearLayoutCompat[@resource-id="com.mx.aseguradoradigital.banorte:id/tercerosAutosBtnInfoVehicle"]'))).click()

            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[1]'))).send_keys("CARLOS")
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[2]'))).send_keys("TEST")
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[3]'))).send_keys("TEST")
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[4]'))).send_keys("30")

            try: self.driver.hide_keyboard() 
            except: pass

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckBox[@resource-id="com.mx.aseguradoradigital.banorte:id/terceroAutoCDPCheckTratamiento"]'))).click()
            
            self.scroll_pequeno()
            time.sleep(1)

            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[2]'))).send_keys("YH178HY32")
            
            try: self.driver.hide_keyboard() 
            except: pass
            time.sleep(1)
            
            # --- LICENCIA (SPINNERS [1] y [2]) ---
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[1]'))).click()
            time.sleep(1)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="Ciudad de México"]'))).click()

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[2]'))).click()
            time.sleep(1)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="Permanente"]'))).click()

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckBox[@resource-id="com.mx.aseguradoradigital.banorte:id/terceroAutoLicenciaPermanente"]'))).click()
            
            # --- SCROLL ENCUADRE PERFECTO ---
            self.scroll_pequeno()
            time.sleep(1)
            self.scroll_muy_pequeno() # <--- Aquí usamos el micro scroll
            time.sleep(2)

            # --- ESTADO, MUNICIPIO, COLONIA Y VÍA (SPINNERS [1], [2], [3], [4]) ---
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[1]'))).click()
            time.sleep(1)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="CIUDAD DE MEXICO"]'))).click()

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[2]'))).click()
            time.sleep(1)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="Coyoacán"]'))).click()

            # --- LÓGICA DE REINTENTO PARA "LA CONCEPCIÓN" ---
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[3]'))).click()
            time.sleep(1)
            try:
                # Intenta buscar "La Concepción" rápidamente
                WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="La Concepción"]'))).click()
            except TimeoutException:
                print("Lista vacía detectada. Cerrando menú y reintentando...")
                self.driver.back() # Cierra el menú desplegable apretando Atrás
                time.sleep(1)
                self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[3]'))).click()
                time.sleep(1)
                self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="La Concepción"]'))).click()

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[4]'))).click()
            time.sleep(1)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="Calle"]'))).click()

            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[2]'))).send_keys("CALLE TEST")
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[3]'))).send_keys("157")
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[5]'))).send_keys("Casa bonita")
            try: self.driver.hide_keyboard() 
            except: pass
            
            self.scroll_pequeno()
            time.sleep(1)

            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[5]'))).send_keys("banortetest@gmail.com")
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[6]'))).send_keys("banortetest@gmail.com")

            try: self.driver.hide_keyboard() 
            except: pass

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="com.mx.aseguradoradigital.banorte:id/terceroCContainerDContacto"]/androidx.appcompat.widget.LinearLayoutCompat/android.widget.RelativeLayout/android.widget.FrameLayout/androidx.appcompat.widget.LinearLayoutCompat/androidx.appcompat.widget.LinearLayoutCompat'))).click()
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"]'))).send_keys("5555555555")
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/dAlertInputBtnOk"]'))).click()

            self.scroll_pequeno()
            time.sleep(1)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@text="AÑADIR FIRMA DIGITAL"]'))).click()
            self.firmar('//android.view.View[@resource-id="com.mx.aseguradoradigital.banorte:id/signaturePad"]')
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/signatureBtnOk"]'))).click()

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/tercerosADConductorBtnSave"]'))).click()
            time.sleep(2) 

            # --- CERRAR POP-UP DE CONDUCTOR ---
            print("Buscando pop-up de Conductor...")
            try:
                wait_rapido = WebDriverWait(self.driver, 4)
                boton_cancelar = wait_rapido.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/dAlertCommonBtnCancel"]')))
                boton_cancelar.click()
                print("Pop-up cerrado.")
                time.sleep(1)
            except (TimeoutException, StaleElementReferenceException):
                print("El pop-up no apareció o se cerró muy rápido, continuando...")

            # ==============================
            # PESTAÑA 2: VEHÍCULO
            # ==============================
            print("Llenando sección Vehículo del Tercero...")
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.LinearLayout[@content-desc="Vehículo"]'))).click()

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[2]'))).click()
            time.sleep(1)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="BENTLEY (AU)"]'))).click()

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[3]'))).click()
            time.sleep(1)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="ARNAGE"]'))).click()

            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[1]'))).send_keys("5555555555")
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[2]'))).send_keys("Y462H17Y")
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[3]'))).send_keys("HSJE762")

            try: self.driver.hide_keyboard() 
            except: pass

            self.scroll_pequeno()
            time.sleep(1)
            
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[4]'))).send_keys("azul")
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[5]'))).send_keys("prueba Test")

            try: self.driver.hide_keyboard() 
            except: pass

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/tercerosADContainerBtnSave"]'))).click()
            time.sleep(2)

            # --- CERRAR POP-UP DE VEHÍCULO ---
            print("Buscando PRIMER pop-up de Vehículo...")
            try:
                wait_rapido = WebDriverWait(self.driver, 4)
                boton_1 = wait_rapido.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/dAlertCommonBtnCancel"]')))
                boton_1.click()
                print("Primer pop-up cerrado.")
                time.sleep(1.5)
            except (TimeoutException, StaleElementReferenceException):
                print("El primer pop-up no apareció o se cerró muy rápido, continuando...")

            # --- CERRAR SEGUNDO POP-UP DE VEHÍCULO (CON PROTECCIÓN) ---
            print("Buscando SEGUNDO pop-up de Vehículo...")
            try:
                wait_rapido = WebDriverWait(self.driver, 4)
                boton_2 = wait_rapido.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/dAlertCommonBtnCancel"]')))
                boton_2.click()
                print("Segundo pop-up cerrado.")
                time.sleep(1.5)
            except (TimeoutException, StaleElementReferenceException):
                print("El segundo pop-up no apareció o se cerró muy rápido, continuando...")

            # ==============================
            # PESTAÑA 3: OCUPANTES
            # ==============================
            print("Llenando sección Ocupantes del Tercero...")
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.LinearLayout[@content-desc="Ocupantes (0)"]'))).click()

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.RadioButton[@resource-id="com.mx.aseguradoradigital.banorte:id/terceroAutoOCheckOcupantesSI"]'))).click()

            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[1]'))).send_keys("EDGAR")
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[2]'))).send_keys("TEST")
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[3]'))).send_keys("TEST")
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[4]'))).send_keys("29")

            try: self.driver.hide_keyboard() 
            except: pass

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.RadioButton[@resource-id="com.mx.aseguradoradigital.banorte:id/terceroAutoOCCheckLesionesSI"]'))).click()

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"]'))).click()
            time.sleep(1)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="Fractura Espalda"]'))).click()

            self.scroll_pequeno()
            time.sleep(1)

            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[2]'))).send_keys("pruebaCorreo@gmail.com")
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[3]'))).send_keys("pruebaCorreo@gmail.com")

            try: self.driver.hide_keyboard() 
            except: pass

            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="com.mx.aseguradoradigital.banorte:id/terceroAutoOContainerDContacto"]/androidx.appcompat.widget.LinearLayoutCompat/android.widget.RelativeLayout/android.widget.FrameLayout/androidx.appcompat.widget.LinearLayoutCompat/androidx.appcompat.widget.LinearLayoutCompat'))).click()
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"]'))).send_keys("5555555555")
            # ... código previo (donde llenas el número de teléfono del ocupante) ...
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/dAlertInputBtnOk"]'))).click()

            # --- GUARDAR OCUPANTES (Una sola vez) ---
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/terceroAutoOContainerBtnSave"]'))).click()
            time.sleep(2)

            # --- REGRESO OBLIGATORIO DESPUÉS DE GUARDAR OCUPANTES ---
            print("Ocupante guardado. Regresando a la pantalla anterior...")
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ImageButton[@content-desc="Navegar hacia arriba"]'))).click()
            time.sleep(2)

            # ==============================
            # PESTAÑA 4: DATOS DEL SEGURO DEL TERCERO
            # ==============================
            print("Llenando sección final del Seguro del Tercero...")
            
            # NOTA: Aquí puse el XPath de Spinner por defecto porque se borró en tu mensaje. 
            # ¡Cámbialo si era otro botón!
            xpath_primer_boton = '(//android.widget.Spinner[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonSpinner"])[1]'
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, xpath_primer_boton))).click()
            time.sleep(1)
            
            # Seleccionar SEGUROS BANORTE
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.CheckedTextView[@resource-id="android:id/text1" and @text="SEGUROS BANORTE GENERALI SA DE CV"]'))).click()

           # Llenar datos de póliza, inciso y teléfono
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[1]'))).send_keys("91H2719HY")
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[2]'))).send_keys("1")
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[3]'))).send_keys("9999999999")

            try: self.driver.hide_keyboard() 
            except: pass

            # --- AQUI USAMOS EL SCROLL MUY PEQUEÑO ---
            self.scroll_muy_pequeno()
            time.sleep(1)

            # --- CÁLCULO DE FECHAS DINÁMICAS ---
            from datetime import datetime, timedelta
            meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
            hoy = datetime.now()
            futuro = hoy + timedelta(days=5)
            
            str_hoy = f"{hoy.day} {meses[hoy.month - 1]} {hoy.year}"
            str_futuro = f"{futuro.day} {meses[futuro.month - 1]} {futuro.year}"
            print(f"Fechas calculadas -> Hoy: {str_hoy} | Futuro: {str_futuro}")

            # Seleccionar Fecha de HOY (Vigencia Desde)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[4]'))).click()
            time.sleep(1)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, f'//android.view.View[@content-desc="{str_hoy}"]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="android:id/button1"]'))).click()

            # --- OTRO SCROLL MUY PEQUEÑO ANTES DE LA SEGUNDA FECHA ---
            self.scroll_muy_pequeno()
            time.sleep(1)

            # Seleccionar Fecha FUTURA (Vigencia Hasta)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[5]'))).click()
            time.sleep(1)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, f'//android.view.View[@content-desc="{str_futuro}"]'))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="android:id/button1"]'))).click()

            self.scroll_hasta_abajo(repeticiones=1) # Le pongo 1 repetición, si le falta ponle 2
            time.sleep(1.5)
            
            # Llenar nombres
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[2]'))).send_keys("RAMON")
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[3]'))).send_keys("TEST")
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"])[4]'))).send_keys("TEST")

            try: self.driver.hide_keyboard() 
            except: pass

            # Añadir teléfono
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//androidx.appcompat.widget.LinearLayoutCompat[@resource-id="com.mx.aseguradoradigital.banorte:id/tercerosPDInputInsuredBtnAddTel"]'))).click()
            self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.mx.aseguradoradigital.banorte:id/vInputCommonEditTxt"]'))).send_keys("5555555555")
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/dAlertInputBtnOk"]'))).click()
            time.sleep(1)

            # Botón final de guardar
            print("Guardando sección completa de Terceros...")
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/tercerosADContainerBtnSave"]'))).click()

            # Aceptar OK del pop-up
            print("Aceptando pop-up final...")
            wait_rapido = WebDriverWait(self.driver, 4)
            wait_rapido.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mx.aseguradoradigital.banorte:id/dAlertCommonBtnOk"]'))).click()
            time.sleep(2)

            print("¡Módulo Terceros completado al 100%!")

        except Exception as e:
            print(f"Error en el módulo de Terceros: {e}")
            try:
                self.driver.find_element(AppiumBy.XPATH, '//android.widget.ImageButton[@content-desc="Navegar hacia arriba"]').click()
            except:
                pass
        finally:
            self.wait = wait_original

    def cerrar_conexion(self):
        if self.driver:
            time.sleep(3)
            self.driver.quit()