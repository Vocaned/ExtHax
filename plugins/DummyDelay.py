import time
from Utils import Plugin, Packet, S2C, C2S

class plugin(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'DummyDelay'
        self.description = 'Create artificial delay, useful for debugging lag based problems on a local server'
        self.S2Ccallbacks = {
            '*': self.s2c,
        }
        self.C2Scallbacks = {
            '*': self.c2s,
        }
        self.onLoad()

    def s2c(self, packet, data):
        time.sleep(0.01)

    def c2s(self, packet, data):
        time.sleep(0.01)