class JagerBotException(Exception):
    pass

class InvalidSpeedError(JagerBotException):
    def __init__(self,speed) -> None:
        self.speed = speed
        super().__init__(f"Speed ({speed}) needs to be between 0 and 255")

class MotorSpeedError(JagerBotException):
    def __init__(left_motor_speed, right_motor_speed, error_direction):
        if error_direction == "left_to_right":
            super().__init__(f"Left motor speed ({left_motor_speed}) cannot be equal to or greater than right motor speed ({right_motor_speed})")
        elif error_direction == "right_to_left":
            super().__init__(f"Right motor speed ({left_motor_speed}) cannot be equal to or greater than left motor speed ({right_motor_speed})")
        
        