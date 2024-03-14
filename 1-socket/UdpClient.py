import socket
import sys


def run_udp_client(port: int, buffer_size: int) -> None:
    HOST = None                 # Symbolic name meaning all available interfaces
    client = None

    for res in socket.getaddrinfo(HOST, port, socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP, socket.AI_PASSIVE):
        af, sock_type, proto, canonname, sa = res
        try:
            client = socket.socket(af, sock_type, proto)

            bytes_to_send = "Hello UDP Server".encode()
            client.sendto(bytes_to_send, sa)

            bytes_from_server = client.recvfrom(buffer_size)
            message = bytes_from_server[0].decode()
            print(f"Message from Server: {message}")
            break

        except OSError as msg:
            print(msg)
            sys.exit(1)

    if client is None:
        print('could not open client socket')
        sys.exit(1)


