class SupersonicUnit:
    def __init__(self, command) -> None:
        self.cmd = command
    
    def horizzontally(self, rotation_angle, pragma = None):
        """
        This function will make the servo move horizontaly to the
        specified rotation angle.

        Parameters:
        rotation_angle(int):        The rotation angle at which the servo will turn
        """
        self.cmd.N = 5
        self.cmd.D1 = 1
        self.cmd.D2 = rotation_angle
        self.cmd.execute_command()

    def vertically(self, rotation_angle):
        """
        This function will make the servo move vertically to the
        specified rotation angle.

        Parameters:
        rotation_angle(int):        The rotation angle at which the servo will turn
        """
        self.cmd.N = 5
        self.cmd.D1 = 2
        self.cmd.D2 = rotation_angle
        self.cmd.execute_command()