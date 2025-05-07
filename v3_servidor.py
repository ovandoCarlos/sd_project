import socket
import threading
import time
from datetime import datetime

# Solicitar al usuario el HOST
#HOST = input("Ingresa la IP del host al que deseas conectarte: ")
#PUERTO = 60500
ARCHIVO_LOG = "mensajes_socket.txt"

def log_mensaje(mensaje):
    #Guardar mensaje en el archivo de log
    with open(ARCHIVO_LOG, 'a', encoding='utf-8') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {mensaje}\n")


def servidor():
    print("Abriendo Sevidor ...\n\n")
    HOST = input("[Servidor] Ingresa la IP del servidor: ")
    PUERTO = int(input("[Servidor] Ingresa el puerto del servidor: "))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PUERTO))
        s.listen()
        print("[Servidor] Escuchando ...\n")

        while True:
            conn, addr = s.accept()
            threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True).start()


def manejar_cliente(conn, addr):
    #"""Función que atiende a cada cliente conectado"""
    with conn:
        print(f"[Servidor] Conectado a {addr}\n\n")
        while True:
            try:
                data = conn.recv(2048)
                if not data:
                    break
                mensaje = data.decode('utf-8')
                print(f"[Servidor] Mensaje recibido de {addr}: {mensaje}\n")
                log_mensaje(f"[Servidor] Mensaje RECIBIDO de {addr}: {mensaje}")
                conn.sendall(f"[Servidor] Mensaje recibido!: {mensaje}".encode('utf-8'))
            except ConnectionResetError:
                print(f"[Servidor] Conexión con {addr} finalizada.")
                break


def cliente():
    print("Ejecutando modo cliente ...\n\n")
    HOST = input("[Cliente] Ingresa el IP del servidor: ")
    PUERTO = int(input("[Cliente] Ingresa el puerto al que se enviarán los mensajes: "))
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
                ss.connect((HOST, PUERTO))
                print("[Cliente] Conexión realizada con el servidor.\n\n")
                
                while True:
                    mensaje = input("[Cliente] Escribe el mensaje que deseas enviar ('salir' para terminar): ")
                    if mensaje.lower() == "salir":
                        print("Finalizando cliente...\n\n")
                        return
                    
                    ss.sendall(mensaje.encode('utf-8'))
                    log_mensaje(f"[Cliente] Enviado a {HOST}: {mensaje}")

                    data = ss.recv(2048)
                    respuesta = data.decode('utf-8')
                    print("Respuesta:", respuesta)
                    log_mensaje(f"Respuesta del servidor: {respuesta}")
        except ConnectionRefusedError:
            print("[Cliente] No se pudo conectar al servidor. Reintentando en 5 segundos...")
            time.sleep(5)

#while True:
threading.Thread(target=servidor, daemon = True).start()

cliente()