import socket
import multiprocessing
import hashlib
import threading

IP = '127.0.0.1'
PORT = 8877
CORES = multiprocessing.cpu_count()
LIST_OF_NUMS = []


def md5_between(start, end, key1, sock):  # check if the md5 existing in the confines
    for z in range(start, end):
        md5_x = hashlib.md5(str(z).encode()).hexdigest()
        if key1 == md5_x:
            print("yes")
            sock.send(bytes(str(key1), "utf-8"))
            sock.close()


while True:
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((IP, PORT))
    x = my_socket.recv(1024).decode()
    print(x)
    list_of_nums = []
    list_of_nums = x.split("%")
    list_of_threads = []
    key = list_of_nums[0]
    x = int(list_of_nums[1])
    y = int(list_of_nums[2])
    i = y - x
    i = int(i / CORES)
    b = 0
    for j in range(CORES):  # open thread to every core
        t = threading.Thread(target=md5_between, args=(x + (i * b), x + (i * (b + 1)), key, my_socket))
        t.start()
        b += 1
        list_of_threads.append(t)
    for t in list_of_threads:  # wait until all the threads done their work and then connect to a new socket
        t.join()
    my_socket.close()
