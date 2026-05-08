import time
from bot_banorte import BotBanorte

def main():
    print("==============================================")
    print("      AUTOMATIZACIÓN DE SINIESTROS BANORTE    ")
    print("==============================================")
    print("Selecciona qué deseas ejecutar:")
    print("1. Ejecutar TODO el proceso")
    print("2. SOLO módulo: Declaraciones")
    print("3. SOLO módulo: Asegurado")
    print("4. SOLO módulo: Deslinde")
    print("5. SOLO módulo: Terceros")
    print("==============================================")
    
    opcion = input("Ingresa el número de tu opción (1-5): ")

    if opcion not in ['1', '2', '3', '4', '5']:
        print("Opción no válida. Cancelando ejecución...")
        return

    # Si la opción es 5, lanzamos el sub-menú antes de perder tiempo conectando al celular
    sub_opcion_terceros = "1"
    if opcion == '5':
        print("\n--- MÓDULO TERCEROS ---")
        print("1. Hacer toda la automatización de terceros")
        print("2. Hacer solo Autos")
        print("3. Hacer solo No Autos")
        sub_opcion_terceros = input("Elige una opción (1-3): ")
        
        if sub_opcion_terceros not in ['1', '2', '3']:
            print("Opción no válida. Cancelando ejecución...")
            return

    print("\nIniciando automatización móvil...")
    bot = BotBanorte(device_name="MiTelefono")
    
    try:
        # Siempre nos conectamos primero, sin importar la opción
        bot.conectar()
        
        # Le damos un par de segundos por si la app está cargando
        time.sleep(3)
        
        # Ejecutar Declaraciones si se eligió TODO (1) o SOLO Declaraciones (2)
        if opcion == '1' or opcion == '2':
            print("\n--- Ejecutando rutina: 1. Declaraciones ---")
            bot.rutina_declaraciones()
            time.sleep(2)
            
        # Ejecutar Asegurado si se eligió TODO (1) o SOLO Asegurado (3)
        if opcion == '1' or opcion == '3':
            print("\n--- Ejecutando rutina: 2. Asegurado ---")
            bot.rutina_asegurado()
            time.sleep(2)

        # Ejecutar Deslinde si se eligió TODO (1) o SOLO Deslinde (4)
        if opcion == '1' or opcion == '4':
            print("\n--- Ejecutando rutina: 3. Deslinde ---")
            bot.rutina_deslinde()
            time.sleep(2)

        # Ejecutar Terceros si se eligió TODO (1) o SOLO Terceros (5)
        if opcion == '1':
            print("\n--- Ejecutando rutina: 4. Terceros ---")
            bot.rutina_terceros(tipo_ejecucion=1)
            time.sleep(2)
        elif opcion == '5':
            print(f"\n--- Ejecutando rutina: 4. Terceros (Sub-opción: {sub_opcion_terceros}) ---")
            bot.rutina_terceros(tipo_ejecucion=int(sub_opcion_terceros))
            time.sleep(2)
            
        print("\n¡Ejecución seleccionada finalizada con éxito!")
            
    except Exception as e:
        print(f"\nOcurrió un error general: {e}")
        
    finally:
        print("Cerrando conexión...")
        bot.cerrar_conexion()

if __name__ == "__main__":
    main()