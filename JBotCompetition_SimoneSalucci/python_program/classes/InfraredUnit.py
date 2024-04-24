class InfraredUnit:
    def __init__(self, command) -> None:
        self.cmd = command


    def off_the_ground(self):
        """
        return(bool):        Return true if the car is off the ground
        """
        self.cmd.N = 23
        self.cmd.execute_command()

    
        