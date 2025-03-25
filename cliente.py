import socket

# Configuración del cliente
SERVER_HOST = '192.168.251.72'  # Cambia a la IP del servidor
SERVER_PORT = 5555        # Puerto del servidor
BUFFER_SIZE = 4096         # Tamaño del buffer para el envío

# Solicitar al usuario el archivo a enviar
file_path = input("Ingresa la ruta del archivo a enviar: ")

try:
    # Crear el socket del cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print(f"[INFO] Conectado al servidor {SERVER_HOST}:{SERVER_PORT}")

    # Enviar el nombre del archivo
    filename = file_path.split('/')[-1]  # Obtener solo el nombre del archivo
    client_socket.sendall(filename.encode())

    # Esperar confirmación del servidor
    response = client_socket.recv(BUFFER_SIZE)
    if response != b"FILENAME_RECEIVED":
        print("[ERROR] No se recibió confirmación del servidor. Cerrando conexión.")
        client_socket.close()
        exit()

    # Enviar el archivo
    with open(file_path, 'rb') as f:
        while chunk := f.read(BUFFER_SIZE):
            client_socket.sendall(chunk)

    print(f"[INFO] Archivo {filename} enviado correctamente")

except FileNotFoundError:
    print("[ERROR] El archivo especificado no existe. Por favor verifica la ruta.")
except Exception as e:
    print(f"[ERROR] Ocurrió un error: {e}")
finally:
    # Cerrar la conexión
    client_socket.close()
