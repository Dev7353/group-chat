
class Config:

    HOST = "192.168.178.27"
    NICKNAME = ""
    PORT = 50000
    PEER = None
    BUDDIES = {
        HOST: ["", False, None],
        "192.168.178.31": ["", False, None],
    }

    def setNickname(self, name):
        self.NICKNAME = name

    def setPeer(self, peer):
        self.PEER=peer

    def addName(self, name, addr):
        for entry in self.BUDDIES:
            if addr[0] == entry:
                self.BUDDIES[entry][0] = name
                return 0
        return -1

    def addPartner(self, conn, addr, name):
        self.BUDDIES[addr[0]] = [name, True, conn]