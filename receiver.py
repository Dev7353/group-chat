import socket, threading

config = None

def recvThread(conn, addr):
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

                if(config.addName(name, addr) == -1):
                    print("[RECEIVER] Socket exists. Append new partner")
                    config.addPartner(conn, addr, name)

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

def recv(conf):
    global config
    config= conf

    receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver.bind((config.HOST, config.PORT))
    receiver.listen(10)

    while(True):
        conn, addr = receiver.accept()
        t = threading.Thread(target=recvThread, args=(conn, addr))
        t.start()



if __name__ == "__main__":
    recv()