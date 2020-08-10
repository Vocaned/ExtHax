from Constants import Plugin, setReturnData

class ExampleCommand(Plugin):
    def __init__(self):
        super().__init__()
        self.name = 'testcom'
        self.description = 'Test Command'
        self.commands = {
            'testcommand': self.testCmd
        }

    def testCmd(self, args):
        print(f'Test command: ARGS {args}')
        setReturnData(None, b'')
