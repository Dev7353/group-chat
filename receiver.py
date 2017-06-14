import socket, threading
from config import *

conf = None

def recvThread(conn, addr): #tcp receive thread
    while(True):
        try:
            data = conn.recv(1024)
            if len(str(data)) == 3: # only b'' is received
                continue
            data_string = str(data)
            data_string = data_string[2:len(data_string)-1]
            if len(data_string) <= 3: # H Message so that slicing works correctly
                conn.send("[RECEIVER] NO MESSAGE. WHATS WRONG WITH YOU?".encode("utf-8"))
                print(data_string)
                continue
            if data_string[0] == 'H' and data_string[1] ==  " ":
                print("[RECEIVER] HELLO REQUEST")
                name = data_string[2:]

                if(conf.addName(name, addr) == -1):
                    print("[RECEIVER] Socket exists. Append new partner")
                    conf.addPartner(conn, addr, name)

                print("[RECEIVER] debug: send OK")
                conn.send("OK".encode("utf-8"))
                print("[RECEIVER] CONNECTION ESTABLISHED")


            elif data_string[0] == 'M' and data_string[1] == " ":
                print("[RECEIVER] MESSAGE REQUEST")
                context  = data_string[2:]
                print(context + " <<")
            else:
                conn.send("[RECEIVER] YOUR MESSAGE DOESNT CORRESPOND WITH THE PROTOCOL.".encode("utf-8"))
                continue

        except socket.timeout:
            conn.close()
            exit(0)
        except socket.error:
            exit(0)

def receiveThreadUDP(receiver):
    global conf

    while True:
        data, addr = receiver.recvfrom(1024)
        data_string = str(data)
        data_string = data_string[2:len(data_string)-1]

        if(data_string[0] == 'H' and data_string[1] == " "):
            print("[RECEIVER] HELLO REQUEST")
            name = data_string[2:]

            if(conf.addName(name, addr) == -1):
                print("[RECEIVER] Socket exists. Append new partner")
                conf.addPartner(receiver, addr, name)

            import time; time.sleep(3)
            receiver.sendto("OK".encode("utf-8"), addr)
            print("[RECEIVER] CONNECTION ESTABLISHED")
        elif(data_string[0] == 'M' and data_string[1] == " "):
            print("[RECEIVER] MESSAGE REQUEST")
            print(data_string[2:] + " <<")
        else:
            return -1


def recv(con):
    global conf
    conf = con

    if(conf.MODE == TCP):
        receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        receiver.bind((conf.HOST, conf.PORT))
        receiver.listen(10)
    else:
        receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receiver.bind((conf.HOST, conf.PORT))

    if(conf.MODE == TCP):
        conn, addr = receiver.accept()
        tcp = threading.Thread(target=recvThread, args=(conn, addr))
        tcp.start()
    else:
        udp = threading.Thread(target=receiveThreadUDP, args=(receiver,))
        udp.start()
