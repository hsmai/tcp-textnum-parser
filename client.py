import argparse
from socket import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, required=True, help="server host")
    parser.add_argument("--port", type=int, required=True, help="server port")
    args = parser.parse_args()

    msg = input("Enter your string: ")
    num = input("Enter a number: ")



    mysock = socket(AF_INET, SOCK_STREAM)
    mysock.connect((args.host, args.port))

    f = mysock.makefile('rwb')


    f.write((msg + '\n').encode())
    f.flush()
    replyA = f.readline().decode().strip()
    print("From Server:", replyA)


    f.write((num + '\n').encode())
    f.flush()
    replyB = f.readline().decode().strip()
    print("From Server:", replyB)

    f.close()
    mysock.close()


if __name__ == "__main__":
    main()