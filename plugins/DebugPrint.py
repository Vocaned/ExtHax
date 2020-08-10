from Constants import Plugin, Packet, S2C, C2S

class plugin(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'DebugPrint'
        self.S2Ccallbacks = {
            '*': self.s2c,
        }
        self.C2Scallbacks = {
            '*': self.c2s,
        }
        self.onLoad()
    
    def s2c(self, packet, data):
        print(f'<- {data.hex()}')
    
    def c2s(self, packet, data):
        print(f'-> {data.hex()}')