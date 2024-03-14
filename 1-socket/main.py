# Echo server program
import time
from multiprocessing import Process

from UdpClient import run_udp_client
from UdpServer import run_udp_server


if __name__ == '__main__':
    port = 50006        # Arbitrary non-privileged port
    buffer_size = 1024  #

    server = Process(target=run_udp_server, args=(port, buffer_size,))
    server.start()

    time.sleep(1.0)
    run_udp_client(port, buffer_size)

    time.sleep(1.0)
    server.terminate()
