import socket, threading

HOST = "192.168.2.104"
PORT = 50000
PEER = None

def recvThread(conn, addr):
    conn.settimeout(100)

    while(True):
        try:
            data = conn.recv(1024)
            if len(str(data)) == 3: # only b'' is received
                continue
            print("RECEIVING")
            data_string = str(data)
            data_string = data_string[2:len(data_string)-1]
            if len(data_string) <= 3: # H Message so that slicing works correctly
                conn.send("NO MESSAGE. WHATS WRONG WITH YOU?".encode("utf-8"))
                print(data_string)
                continue
            if data_string[0] == 'H' and data_string[1] ==  " ":
                print("HELLO REQUEST")
                name = data_string
                assert PEER.send((name + "|" + addr[0]).encode("utf-8")) > 0
            elif data_string[0] == 'M' and data_string[1] == " ":
                print("MESSAGE REQUEST")
                context  = data_string[2:]
                PEER.send(context.encode("utf-8"))
            else:
                conn.send("YOUR MESSAGE DOESNT CORRESPOND WITH THE PROTOCOL.".encode("utf-8"))
                continue

        except socket.timeout:
            conn.close()
            exit(0)
        except socket.error:
            exit(0)

def recv():
    global PEER, HOST, PORT
    receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver.bind((HOST, PORT))
    receiver.listen(5)

    conn, addr = receiver.accept()
    PEER = conn
    while(True):
        conn, addr = receiver.accept()
        t = threading.Thread(target=recvThread, args=(conn, addr))
        t.start()



if __name__ == "__main__":
    recv()