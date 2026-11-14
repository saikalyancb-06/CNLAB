import socket
import os

HOST = '127.0.0.1'
PORT = 65432

# Always look for files in the exact folder where server.py is saved
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server listening on {HOST}:{PORT}...")

    # Keep the server running for multiple client requests
    while True:
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            filename = conn.recv(1024).decode().strip()
            filepath = os.path.join(BASE_DIR, filename)

            if os.path.isfile(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    if not content:
                        conn.sendall(b"[File is empty]")
                    else:
                        conn.sendall(content.encode('utf-8'))
                except UnicodeDecodeError:
                    conn.sendall(b"Error: Cannot read binary files (like PDFs) as plain text.")
            else:
                conn.sendall(b"File not found.")
