# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# Curso: PROGRAMACIÓN (213023)
# Fase 4: PRÁCTICAS SIMULADAS
# Trabajo: SISTEMA INTEGRAL SOFTWARE FJ
# Nombre del producto: servicios.py
# Estudiante: Karen Lizeth Gonzalez Cante

# Módulo de Registro de Logs (logger.py)
# Registra todos los eventos, advertencias y errores del sistema 
# en un archivo de texto plano (sistema_fj.log).

import os
from datetime import datetime

NOMBRE_ARCHIVO_LOG = "sistema_fj.log"

def registrar_log(mensaje: str, nivel: str = "INFO"):
    # Registra un mensaje en el archivo de logs con la fecha y hora actuales.
    # Niveles soportados: INFO, WARNING, ERROR
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea_log = f"[{timestamp}] [{nivel.upper()}] {mensaje}\n"
    
    try:
        # Abre el archivo en modo 'append' (añadir al final) para no sobrescribir registros previos
        with open(NOMBRE_ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
            archivo.write(linea_log)
    except Exception as e:
        print(f"[ERROR CRÍTICO EN LOGGER] No se pudo escribir en el archivo de log: {e}")


if __name__ == "__main__":
    ejecutar_simulacion()
