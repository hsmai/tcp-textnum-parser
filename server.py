import argparse
from socket import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True, help="port to listen on")
    parser.add_argument("--number", type=int, required=True, help="server number")
    args = parser.parse_args()

    # create and bind TCP socket
    server_Socket = socket(AF_INET, SOCK_STREAM)
    server_Socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


    # bind and listen
    server_Socket.bind(('', args.port))
    server_Socket.listen(5)

    print(f"Server ready... listening on port {args.port}, server number={args.number}")

    while True:

        connection_Socket, addr = server_Socket.accept()

        f = connection_Socket.makefile('rwb')

        msg = f.readline().decode().rstrip('\r\n')
        print("Received string:", msg)


        f.write((msg.upper() + '\n').encode())
        f.flush()

        num = f.readline().decode().strip()
        print("Received number:", num)


        total = int(num) + args.number
        f.write((str(total) + '\n').encode())
        f.flush()

        f.close()
        connection_Socket.close()

if __name__ == "__main__":
    main()