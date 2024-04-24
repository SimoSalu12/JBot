from classes.exceptions.JagerBotException import InvalidSpeedError
from classes.exceptions.JagerBotException import MotorSpeedError
class Movement:
    def __init__(self, command) -> None:
        self.cmd = command

    def forward(self, speed):
        if speed < 0 or speed > 255:
            raise InvalidSpeedError(speed)
        self.cmd.D1 =  3
        self.cmd.D2 = speed # 0 ~ 255
        self.cmd.execute_command()

    def backword(self, speed):
        if speed < 0 or speed > 255:
            raise InvalidSpeedError(speed)
        self.cmd.D1 = 4
        self.cmd.D2 = speed # 0 ~ 255
        self.cmd.execute_command()

    def right(self, left_motor_speed = None, right_motor_speed = None, speed = None):
        if speed:
            if speed < 0 or speed > 255:
                raise InvalidSpeedError(speed)
            self.cmd.D1 = 2
            self.cmd.D2 = speed
        else:
            if right_motor_speed >= left_motor_speed:
                raise MotorSpeedError(left_motor_speed, right_motor_speed, 'right-to-left')
            if right_motor_speed < 0 or right_motor_speed > 255:
                raise InvalidSpeedError(speed)
            if left_motor_speed < 0 or left_motor_speed > 255:
                raise InvalidSpeedError(speed)
            self.cmd.N = 4
            self.cmd.D2 = left_motor_speed # 0 ~ 255
            self.cmd.D1 = right_motor_speed # 0 ~ 255

        self.cmd.execute_command()

    def left(self, left_motor_speed = None, right_motor_speed = None, speed = None):
        if speed:
            if speed < 0 or speed > 255:
                raise InvalidSpeedError(speed)
            self.cmd.D1 = 1
            self.cmd.D2 = speed
        else:
            if left_motor_speed >= right_motor_speed:
                raise MotorSpeedError(left_motor_speed, right_motor_speed, 'left-to-right')
            if right_motor_speed < 0 or right_motor_speed > 255:
                raise InvalidSpeedError(speed)
            if left_motor_speed < 0 or left_motor_speed > 255:
                raise InvalidSpeedError(speed)
            self.cmd.N = 4
            self.cmd.D2 = left_motor_speed # 0 ~ 255
            self.cmd.D1 = right_motor_speed # 0 ~ 255
        
        self.cmd.execute_command()