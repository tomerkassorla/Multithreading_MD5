import socket
import hashlib
import threading

IP = '127.0.0.1'
PORT = 8877
REQUEST = "t"


def rcv_func(sock):  # receive
    x = sock.recv(1024).decode()
    print(x)
    global REQUEST
    if x != "":
        REQUEST = x


def client_accept(x, y, md5_x, sock, dig):  # after client accept send him the confines
    print("send to client")
    sock.send(bytes(md5_x + "%" + str(1 * (10 ** (dig - 1)) + y * x) + "%" + str(1 * (10 ** (dig - 1)) + (y + 1) * x),
                    "utf-8"))
    quit()


def main():
    dig = int(input("enter how much digits you have in your number"))
    n = str(input("enter your number"))
    global REQUEST
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(10)
    md5_x = hashlib.md5(n.encode()).hexdigest()
    print(md5_x)
    x = int(9 * (10 ** (int(dig) - 1)) / 10)
    ok = True
    y = 0
    while ok:  # open thread to every clint that connect to send him the confines, and open thread to received from every client
        client_socket, address = server_socket.accept()
        t = threading.Thread(target=client_accept, args=(x, y, md5_x, client_socket, dig))
        t.start()
        y += 1
        print(y)
        t = threading.Thread(target=rcv_func, args=(client_socket,))
        t.start()
        if y == 10:
            ok = False
        if REQUEST != "t":
            ok = False


if __name__ == '__main__':
    main()
