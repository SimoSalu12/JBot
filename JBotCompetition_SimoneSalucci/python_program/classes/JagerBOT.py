from classes.Movement import Movement
from classes.Command import Command
from classes.SupersonicUnit import SupersonicUnit
from classes.UltrasonicUnit import UltrasonicUnit
from classes.InfraredUnit import InfraredUnit
from classes.Camera import Camera
from classes.Mode import Mode
from socket import socket as Socket
import sys

class JagerBOT:
    def __init__(self) -> None:
        self.command_counter = 0
        self.socket = self.connect()

    def move(self):
        cmd = self.initialize_command()
        cmd.N = 3
        return Movement(cmd)
    
    def stop(self):
        cmd = self.initialize_command()
        cmd.N = 1
        cmd.D1 = 0
        cmd.D2 = 0
        cmd.D3 = 1
        cmd.execute_command()

    def rotate(self):
        cmd = self.initialize_command()
        return SupersonicUnit(cmd)
    
    def measure(self):
        cmd = self.initialize_command()
        cmd.N = 21
        return UltrasonicUnit(cmd)
    
    def detect(self):
        cmd = self.initialize_command()
        cmd.N = 21
        return UltrasonicUnit(cmd)
    
    def check(self):
        cmd = self.initialize_command()
        return InfraredUnit(cmd)

    def camera(self):
        cmd = self.initialize_command()
        return Camera(cmd)
    
    def restart(self):
        """
        Clear all the functions being executed, and do not enter the standby mode.
        """
        cmd = self.initialize_command()
        cmd.N = 110
        cmd.execute_command()

    def follow(self):
        cmd = self.initialize_command()
        return InfraredUnit(cmd)
    
    def mode(self):
        cmd = self.initialize_command()
        return Mode(cmd)
    
    def close_connection(self):
        cmd = self.initialize_command()
        cmd.N = 404
        print(cmd)
        self.socket.close()

    def initialize_command(self):
        self.command_counter += 1
        return Command(self.command_counter, self.socket)
    
    def connect(self):
        ip = "192.168.4.1"
        port = 100
        print('Connecting to {0}:{1}'.format(ip, port))
        socket = Socket()
        try: 
            socket.connect((ip,port))
            print('Connected!')
            self.test_connection(socket, ip, port)
            return socket
        except Exception as e:
            print('Error: ', e)
            sys.exit()

    def read_output(self):
        cmd = self.initialize_command()
        return cmd.read_output()

    def test_connection(self, socket, ip, port):
        print('Receive from {0}:{1}'.format(ip, port))
        try:
            data = socket.recv(1024).decode()
        except Exception as e:
            print('Error: ', e)
            sys.exit()
        print('Received: ', data)
    

        
