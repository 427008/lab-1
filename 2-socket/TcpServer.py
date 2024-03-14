import socket
import sys
from math import sqrt


def create_server() -> socket:
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('127.0.0.1', 0, ))
        server.listen(1)
    except OSError as msg:
        print(msg)
        sys.exit(1)

    if server is None:
        print('could not open server socket')
        sys.exit(1)

    return server

def run_server_connection(server: socket) -> None:
    print('Wait...')
    conn, addr = server.accept()
    with conn:
        print('Connected by', addr)
        data = "Уравнение Пифагора a2+b2=c2\nВведите a:".encode('utf-8')
        a = None
        b = None
        conn.send(data)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            if a is None:
                # TODO check if data is float
                a = float(data.decode('utf-8'))
                data = f"Получено {a:.2f}\nВведите b:".encode('utf-8')
                conn.send(data)
                continue
            if b is None:
                # TODO check if data is float
                b = float(data.decode('utf-8'))
                c = sqrt((a * a + b * b))
                data = f"Получено {b:.2f}\nРешение: с = {c:.5f}".encode('utf-8')
                conn.send(data)
                break
            # next loop (data is not float)

    server.close()
