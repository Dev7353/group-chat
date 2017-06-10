import socket, receiver, threading
from config import *

conf = None

def peer():
    global conf
    scanflag = False
    NICKNAME = input("NICKNAME: ")
    conf = Config()
    conf.setNickname(NICKNAME)
    PEER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PEER.connect_ex((conf.HOST, conf.PORT))
    conf.setPeer(PEER)

    scanner = threading.Thread(target=scanThread)
    receiverThread =threading.Thread(target=receiver.recv, args=(conf,))
    receiverThread.start()

    while(True):
        print("M: Message")
        print("G: Group Message")
        print("L: List of Buddies")
        print("Q: Quit")
        print("S: Scan")
        i = input("> ")
        cleanDisplay()
        if len(i) < 1:
            print("PLEASE SELECT YOUR OPTION")
            continue
        if i == 'Q':
            break
        elif i == 'L':
            print(str(conf.BUDDIES))
        elif i  == 'S':
            if scanflag == True:
                print("Your scanner is already running")
                continue
            scanflag = True
            scanner.start()
        elif i[0] == 'M':
            print(str(conf.BUDDIES))
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
                for entry in conf.BUDDIES:
                    if conf.BUDDIES[entry][1] == True:
                       conf.BUDDIES[entry][2].send(("M " + msg).encode("utf-8"))

def getSocket(buddy):
    for entry in conf.BUDDIES:
        if conf.BUDDIES[entry][0] == buddy:
            return conf.BUDDIES[entry][2]

    return None

def cleanDisplay():
    for i in range(25):
        print()

def scanThread():
    global conf
    while(True):
        for entry in conf.BUDDIES:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if conf.BUDDIES[entry][1] == False and s.connect_ex((entry, conf.PORT)) == 0:
                print("[SCANNER] NEW BUDDY: [" + entry + "]")
                conf.BUDDIES[entry][1] = True
                conf.BUDDIES[entry][2] = s
                s.send(("H " + conf.NICKNAME).encode("utf-8"))
                data_string = str(s.recv(1024))

                if("OK" in data_string):
                    print("[SCANNER] CONNECTION ESTABLISHED")

            elif conf.BUDDIES[entry][1] == True:
                try:
                    conf.BUDDIES[entry][2].send("".encode("utf-8"))
                except socket.error:
                    print("DISCONNECT FROM BUDDY: [" + entry + "]")
                    conf.BUDDIES[entry][1] = False
                    conf.BUDDIES[entry][2] = None
                    s.close()
            else:
                s.close()

if __name__ == '__main__':
    peer()