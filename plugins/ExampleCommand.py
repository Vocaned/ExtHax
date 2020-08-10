from Constants import Plugin, setReturnData

class plugin(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'testcom'
        self.description = 'Test Command'
        self.commands = {
            'testcommand': self.testCmd
        }
        self.onLoad()

    def testCmd(self, args):
        print(f'Test command: ARGS {args}')
