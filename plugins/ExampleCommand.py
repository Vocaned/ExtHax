from Constants import Command


class ExampleCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = 'testcommand'
        self.description = 'Test Command'
        self.help = f'{self.name} - {self.description}'

    def call(self, returndata, args):
        print(f'Test command: ARGS {args}')
        return [returndata[0], b'']
