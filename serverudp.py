import socket
import os

HOST = '127.0.0.1'
PORT = 65432

# Always look for files in the exact folder where udp_server.py is saved
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind((HOST, PORT))
    print(f"UDP Server listening on {HOST}:{PORT}...")

    while True:
        data, client_addr = server_socket.recvfrom(1024)
        filename = data.decode().strip()
        print(f"Request for '{filename}' from {client_addr}")
        
        filepath = os.path.join(BASE_DIR, filename)

        if os.path.isfile(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                if not content:
                    server_socket.sendto(b"[File is empty]", client_addr)
                else:
                    server_socket.sendto(content.encode('utf-8'), client_addr)
            except UnicodeDecodeError:
                server_socket.sendto(b"Error: Cannot read binary files as plain text.", client_addr)
        else:
            server_socket.sendto(b"File not found.", client_addr)
