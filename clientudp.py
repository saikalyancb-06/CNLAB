import socket

HOST = '127.0.0.1'
PORT = 65432

filename = input("Enter file name to request: ")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    client_socket.settimeout(5.0)
    client_socket.sendto(filename.encode('utf-8'), (HOST, PORT))
    
    try:
        data, _ = client_socket.recvfrom(4096)
        print("\n--- File Content ---")
        print(data.decode('utf-8'))
    except socket.timeout:
        print("\nError: Request timed out. Make sure udp_server.py is running.")
