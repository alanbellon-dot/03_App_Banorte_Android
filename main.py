import time
from bot_banorte import BotBanorte

def main():
    print("Iniciando automatización móvil completa...")
    
    bot = BotBanorte(device_name="MiTelefono")
    
    try:
        bot.conectar()
        
        # Le damos un par de segundos por si la app está cargando
        time.sleep(3)
        
        print("--- Ejecutando rutina: 1. Declaraciones ---")
        bot.rutina_declaraciones()
        
        # Pequeña pausa entre módulos por si la app tiene alguna animación de carga
        time.sleep(2)
        
        print("--- Ejecutando rutina: 2. Asegurado ---")
        bot.rutina_asegurado()
        
        # Pequeña pausa antes de iniciar el tercer módulo
        time.sleep(2)

        print("--- Ejecutando rutina: 3. Deslinde ---")
        bot.rutina_deslinde()
            
    except Exception as e:
        print(f"Ocurrió un error general: {e}")
        
    finally:
        print("Cerrando conexión...")
        bot.cerrar_conexion()

if __name__ == "__main__":
    main()