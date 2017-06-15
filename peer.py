import socket
import receiver
import threading
from config import *
conf = None


def peer():
    global conf

    conf = Config()
    scanflag = False
    MODE = TCP
    PEER = None

    MODE = input("Configure your Mode [TCP/UDP]: ")

    NICKNAME = input("NICKNAME: ")
    conf = Config()
    assert conf.setMode(MODE) == 0
    assert conf.setNickname(NICKNAME) == 0
    assert conf.setPeer(PEER) == 0

    if(MODE == TCP):
        scanner = threading.Thread(target=scanThread)
    else:
        scanner = threading.Thread(target=scanThreadUdp)

    receiverThread = threading.Thread(target=receiver.recv, args=(conf,))
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
        elif i == 'S':
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
                if(MODE == TCP):
                    getSocket(BUDDY).send(("M " + msg).encode("utf-8"))
                else:
                    counter = 0
                    getSocket(BUDDY).settimeout(2)
                    while(counter < 10):
                        getSocket(BUDDY).sendto(
                            ("M " + msg).encode("utf-8"), getAddr(BUDDY))
                        try:
                            getSocket(BUDDY).recvfrom(1024)
                            break
                        except socket.timeout:
                            print("[PEER] CONNECTION LOST. TRY AGAIN...")
                            counter += 1

                    if(counter == 9):
                        print("[PEER] CONNECTION PARTNER DOWN")
                        # remove from buddy list
        elif i[0] == 'G':
            while True:
                msg = input(">> ")
                if msg == 'Q':
                    break
                for entry in conf.BUDDIES:
                    if(MODE == TCP):
                        getSocket(
                            conf.BUDDIES[entry][0]).send(
                            ("M " + msg).encode("utf-8"))
                    else:
                        BUD = conf.BUDDIES[entry][0]
                        getSocket(BUD).sendto(
                            ("M " + msg).encode("utf-8"), getAddr(BUD))


def getSocket(buddy):
    global conf
    for entry in conf.BUDDIES:
        if conf.BUDDIES[entry][0] == buddy:
            return conf.BUDDIES[entry][2]

    return None


def getAddr(buddy):
    global conf
    for entry in conf.BUDDIES:
        if conf.BUDDIES[entry][0] == buddy:
            return entry, conf.PORT

    return None


def cleanDisplay():
    for i in range(25):
        print()


def scanThread():
    global conf
    while(True):
        for entry in conf.BUDDIES:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if conf.BUDDIES[entry][1] == False and s.connect_ex(
                    (entry, conf.PORT)) == 0:
                print("[SCANNER] NEW BUDDY: [" + entry + "]")
                s.send(("H " + conf.NICKNAME).encode("utf-8"))
                print("[SCANNER] RECEIVE ACKNOWLEDGEMENT")
                data_string = str(s.recv(1024))

                if("OK" in data_string):
                    print("[SCANNER] CONNECTION ESTABLISHED: " + entry)
                    conf.BUDDIES[entry][1] = True
                    conf.BUDDIES[entry][2] = s
                else:
                    print("[SCANNER] CONNECTION FAILED: " + entry)

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


def scanThreadUdp():
    global conf
    while(True):
        for entry in conf.BUDDIES:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            if conf.BUDDIES[entry][1] == False:
                reachable = False
                s.sendto(
                    ("H " + conf.NICKNAME).encode("utf-8"), (entry, conf.PORT))
                data_string = ""
                while(reachable == False):
                    try:
                        data_string = str(s.recvfrom(1024))
                        reachable = True
                        break
                    except socket.timeout:
                        reachable = False
                        break

                if(reachable == True):
                    print("[SCANNER] NEW BUDDY: [" + entry + "]")
                    conf.BUDDIES[entry][1] = True
                    conf.BUDDIES[entry][2] = s

                    if("OK" in data_string):
                        print("[SCANNER] CONNECTION ESTABLISHED")

                else:
                    s.close()
            else:
                s.close()

if __name__ == '__main__':
    peer()
