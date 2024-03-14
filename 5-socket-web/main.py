import argparse

from MyHTTPServer import MyHTTPServer


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bind', '-b', metavar='ADDRESS',
                        default='127.0.0.1', type=str,
                        help='Specify alternate bind address '
                             '[default: all interfaces]')
    parser.add_argument('port', action='store',
                        default=8000, type=int,
                        nargs='?',
                        help='Specify alternate port [default: 8000]')
    parser.add_argument('name', action='store',
                        default='', type=str,
                        nargs='?',
                        help='Specify alternate name [default: bind address]')
    args = parser.parse_args()

    host = args.bind
    port = args.port
    name = args.name if args.name != '' else args.bind
    serv = MyHTTPServer(host, port, name)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
