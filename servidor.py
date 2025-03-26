import socket

# Configuración del servidor
HOST = '0.0.0.0'  # Escucha en todas las interfaces
PORT = 5555     # Puerto de escucha
BUFFER_SIZE = 4096 # Tamaño del buffer para la recepción

# Crear el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"[INFO] Servidor escuchando en {HOST}:{PORT}")

while True:
    print("[INFO] Esperando conexión...")
    conn, addr = server_socket.accept()
    print(f"[INFO] Conexión aceptada de {addr}")

    try:
        # Recibir el nombre del archivo
        filename = conn.recv(BUFFER_SIZE).decode(errors="ignore").strip()
        print(f"[INFO] Nombre del archivo recibido: {filename}")

        # Confirmar recepción del nombre del archivo
        conn.sendall(b"FILENAME_RECEIVED")

        # Recibir el archivo y guardarlo
        with open(filename, 'wb') as f:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:  # Fin de la transmisión
                    break
                f.write(data)

        print(f"[INFO] Archivo '{filename}' recibido y guardado correctamente.")

    except Exception as e:
        print(f"[ERROR] Ocurrió un error: {e}")

    finally:
        conn.close()
        print("[INFO] Conexión cerrada")

# Cerrar el socket del servidor (nunca se alcanza en este bucle)
server_socket.close()
