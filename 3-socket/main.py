# Echo server program
import time
from multiprocessing import Process

from TcpClient import run_tcp_client
from TcpServer import run_server_connection, create_server

if __name__ == '__main__':
    server = create_server()
    laddr = server.getsockname()
    # laddr[0] is '127.0.0.1'
    port = laddr[1]

    srv_process = Process(target=run_server_connection, args=(server,))
    srv_process.start()
    # server ready for connection
    time.sleep(1.0)

    # enter pythagoras
    run_tcp_client(port, buffer_size=1024)

    srv_process.join()
    srv_process.terminate()
