import sys
import time
from bot_banorte import BotBanorte

def main():
    # Revisamos si el .bat nos mandó algún número
    if len(sys.argv) > 1:
        opcion_elegida = sys.argv[1]
    else:
        opcion_elegida = "1" # Por defecto ejecutará Declaraciones

    print(f"Iniciando automatización móvil... (Módulo: {opcion_elegida})")
    
    bot = BotBanorte(device_name="MiTelefono")
    
    try:
        bot.conectar()
        
        # Le damos un par de segundos por si la app está cargando
        time.sleep(3)
        
        if opcion_elegida == "1":
            print("Ejecutando rutina: 1. Declaraciones")
            bot.rutina_declaraciones()
        elif opcion_elegida == "2":
            print("Ejecutando rutina: 2. Asegurado (En Proceso)")
        elif opcion_elegida == "3":
            print("Ejecutando rutina: 3. Deslinde de responsabilidades (En Proceso)")
        elif opcion_elegida == "4":
            print("Ejecutando rutina: 4. Estimacion daños y lesiones (En Proceso)")
        elif opcion_elegida == "5":
            print("Ejecutando rutina: 5. Terceros (En Proceso)")
        elif opcion_elegida == "6":
            print("Ejecutando rutina: 6. Volantes Digitales (En Proceso)")
        elif opcion_elegida == "7":
            print("Ejecutando rutina: 7. Cierre (En Proceso)")
        elif opcion_elegida == "8":
            print("Ejecutando rutina: 8. Realizar toda la operación (En Proceso)")
        else:
            print(f"La opción {opcion_elegida} no es válida o aún no está programada.")
            
    except Exception as e:
        print(f"Ocurrió un error general: {e}")
        
    finally:
        bot.cerrar_conexion()

if __name__ == "__main__":
    main()