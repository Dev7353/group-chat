TCP = "TCP"
UDP = "UDP"

class Config:
    MODE = ""
    HOST = "141.37.202.37"
    NICKNAME = ""
    PORT = 50000
    PEER = None
    BUDDIES = {
        #HOST: ["", False, None],
        "141.37.168.35": ["", False, None],
    }

    def setMode(self, mode):
        if((mode != TCP) and (mode != UDP)):
            return -1
        self.MODE = mode
        return 0

    def setNickname(self, name):
        self.NICKNAME = name
        return 0

    def setPeer(self, peer):
        self.PEER=peer
        return 0

    def addName(self, name, addr):
        for entry in self.BUDDIES:
            if addr[0] == entry:
                self.BUDDIES[entry][0] = name
                return 0
        return -1

    def addPartner(self, conn, addr, name):
        self.BUDDIES[addr[0]] = [name, True, conn]