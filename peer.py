import threading, socket
HOST = "127.0.0.1"
PORT = 50000
BUDDY = None
NICKNAME = ""
PEER = None
BUDDIES = {
    "127.0.0.1": ["", False, None]
}

def outputThread():
    global PEER, BUDDIES
    while(True):
        print(PEER)
        data = PEER.recv(1024)
        if len(str(data)) == 3:
            continue
        data = str(data)[2:len(str(data))-1]

        if data[0] == 'H' and data[1] == ' ':
            name, ip = data[2:].split("|")
            BUDDIES[ip][0] = name
            print("UPDATE BUDDY LIST. NEW NAME: " + name)
        else:
            print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t " + data + " <")


def scanThread():
    global PORT
    while(True):
        for entry in BUDDIES:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if BUDDIES[entry][1] == False and s.connect_ex((entry, PORT)) == 0:
                print("NEW BUDDY: [" + entry + "]")
                BUDDIES[entry][1] = True
                BUDDIES[entry][2] = s
                s.send(("H " + NICKNAME).encode("utf-8"))
            elif BUDDIES[entry][1] == True:
                try:
                    BUDDIES[entry][2].send("".encode("utf-8"))
                except socket.error:
                    print("DISCONNECT FROM BUDDY: [" + entry + "]")
                    BUDDIES[entry][1] = False
                    BUDDIES[entry][2] = None
                    s.close()
            else:
                s.close()
def peer():
    global NICKNAME, PEER
    NICKNAME = input("NICKNAME: ")
    scanner = threading.Thread(target=scanThread)
    PEER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    assert PEER.connect_ex((HOST, PORT)) == 0
    output = threading.Thread(target=outputThread)
    output.start()
    scanner.start()

    while(True):
        print("M: Message")
        print("G: Group Message")
        print("L: List of Buddies")
        print("Q: Quit")
        i = input("> ")
        cleanDisplay()
        if len(i) < 1:
            print("PLEASE SELECT YOUR OPTION")
            continue
        if i == 'Q':
            PEER.send("QUIT".encode("utf-8"))
            break
        elif i == 'L':
            print(str(BUDDIES))
        elif i[0] == 'M':
            print(str(BUDDIES))
            BUDDY = input("CHOOSE YOUR BUDDY: ")
            print("SEND YOUR MESSAGE")
            while(True):
                msg = input(">> ")
                if msg == 'Q':
                    break
                getSocket(BUDDY).send(("M " + msg).encode("utf-8"))

        elif i[0] == 'G':
            while True:
                msg = input(">> ")
                if msg == 'Q':
                    break
                for entry in BUDDIES:
                    if BUDDIES[entry][1] == True:
                        BUDDIES[entry][2].send(("M " + msg))

def getSocket(buddy):
    for entry in BUDDIES:
        if BUDDIES[entry][0] == buddy:
            return BUDDIES[entry][2]

    return None

def cleanDisplay():
    for i in range(25):
        print()

if __name__ == '__main__':
    peer()