import paramiko


class SSH:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def connect(self):
        print(f'Connecting to {self.host}...')
        # Code to connect to the host

    def execute(self, command):
        print(f'Executing command: {command}')
        # Code to execute the command

    def close(self):
        print(f'Closing connection to {self.host}')
        # Code to close the connection