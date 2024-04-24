from socket import socket as Socket
import time
import json
import sys
import re

class Command:
    """
    Represents a command for controlling jagerBOT.

    Attributes:
        id (int):                       The identifier of the command.
        socket (object):                The socket used for communication.
        N (int):                        The robot unit that will follow the command instruction.
        D1 (int):                       The first parameter.
        D2 (int):                       The second parameter.
        D3 (int):                       The third parameter.
    """
    
    def __init__(self, id:int, socket:object, N:int = None, D1:int = None, D2:int = None, D3:int = None) -> None:
        """
        This function will construct a new Command object.

        Parameters:
            id (int):                       The identifier of the command.
            socket:                         The socket used for communication.
            N (int):                        The robot unit that will follow the command instruction.
            D1 (int):                       The first parameter.
            D2 (int):                       The second parameter.
            D3 (int):                       The third parameter.

        Note: D1, D2, and D3 parameters can rappresent different values depending on the 
        unit that the command will target. 
        Check the "\code\program\data\commandMapList.json" for better information
        """
        self.id = id
        self.socket = socket
        self.N = N
        self.D1 = D1
        self.D2 = D2
        self.D3 = D3

    def __str__(self) -> str:
        try:
            command_map_list = self.get_command_map_list()

            # Car | move forward/backward Supersonic unit | rotate horizzontally/vertically
            if self.N == 3 or self.N == 5 or self.N == 1:
                return (f'{self.id}: {command_map_list["command_number"][str(self.N)]["unit"]} ' 
                f'{command_map_list["command_number"][str(self.N)]["action"][str(self.D1)]} '
                f'at {self.D2}')
            
            # Car | move left/right
            if self.N == 4:
                return (f'{self.id}: {command_map_list["command_number"][str(self.N)]["unit"]} '
                f'{command_map_list["command_number"][str(self.N)]["action"]} '
                f'left at {self.D2}, right at {self.D1})')
            
            # Ultrasonic unit | measure/detect 
            if self.N == 21:
                return (f'{self.id}: {command_map_list["command_number"][str(self.N)]["unit"]} '
                f'{command_map_list["command_number"][str(self.N)]["action"][str(self.D1)]}')
            
            # Follow black line
            if self.N == 101:
                return (f'{self.id}: {command_map_list["command_number"][str(self.N)]["unit"]} '
                f'{command_map_list["command_number"][str(self.N)]["action"][str(self.D1)]}')
            
            # Infrared unit | check off the ground + Car | restart + Camera | capture image
            if self.N == 23 or self.N == 110 or self.N == 111 or self.N == 404:
                return (f'{self.id}: {command_map_list["command_number"][str(self.N)]["unit"]} '
                f'{command_map_list["command_number"][str(self.N)]["action"]}')

            # Measure motion
            if self.N == 6:
                return f'{self.id}: Car measure motion'
            
            # Adjust sensibility
            if self.N == 104:
                return f'{self.id} Adjust infrared unit sensibility to {self.D1}'
            
            # Check infrared sensor value
            if self.N == 22:
                return f'{self.id} Check infrared sensor values'

        except Exception as e:
            print('Error: ', e)
            sys.exit()


    def execute_command(self, pragma = None, timeout=None):
        try:
            # Invia il comando al socket
            self.socket.send(self.format_command().encode())

            # Decodifica l'output e lo ritorna se presente
            if not pragma:
                print(self.__str__())
                while 1:
                    output = self.socket.recv(1024).decode()
                    if '_' in output:
                        break
                output = self.decode_output(output)
                return output if output else None

            # Resta in ascolto per il tempo indicato
            if pragma == 'timeout':
                if not timeout:
                    print(self.__str__())
                    # self.socket.recv(1024).decode()
                else:
                    star_time = time.time()
                    end_time = star_time + timeout
                    print(self.__str__())
                    while time.time() < end_time:
                        pass
                        # self.socket.recv(1024).decode()

        except Exception as e:
            print('Error: ', e)
            sys.exit()
        

    def format_command(self):
            command_dict = {'H': str(self.id)}
            if self.N:
                command_dict['N'] = self.N
            if self.D1:
                command_dict['D1'] = self.D1
            if self.D2:
                command_dict['D2'] = self.D2
            if self.D3:
                command_dict['D3'] = self.D3
            return json.dumps(command_dict)

    def get_command_map_list(self):
        with open('code/program/data/commandMapList.json', 'r') as json_file:
            return json.load(json_file)
        


    def decode_output(self, output):
        try:
            output = re.search('_(.*)}', output).group(1)
        except Exception as e:
            print('received:', output)
            return 
        
        if output in ['ok', 'true']:
            return 1
        elif output == 'false':
            return 0
        
        return output
    
    def read_output(self):
        output = self.socket.recv(1024).decode()
        output = self.decode_output(output)
        time.sleep(0.5)
        return output

        

