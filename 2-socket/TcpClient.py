import socket
import sys


def run_tcp_client(port: int, buffer_size: int) -> None:
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', port, ))
    except OSError as msg:
        print(msg)
        sys.exit(1)

    if client is None:
        print('could not open client socket')
        sys.exit(1)

    with client:
        data = client.recv(buffer_size)
        print(data.decode('utf-8'))
        a = float(input())
        data = f'{a}'.encode('utf-8')
        client.sendall(data)
        data = client.recv(buffer_size)
        print(data.decode('utf-8'))
        b = float(input())
        data = f'{b}'.encode('utf-8')
        client.sendall(data)
        data = client.recv(buffer_size)
        print(data.decode('utf-8'))
