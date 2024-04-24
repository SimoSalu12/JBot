class Mode:
    def __init__(self, command) -> None:
        self.cmd = command

    def follow_black_line(self, timeout=None):
        """
        params:
        timeout(int):       The timeout of the follow black line mode
        """
        self.cmd.N = 101
        self.cmd.D1 = 1
        self.cmd.D2 = 2
        self.cmd.execute_command('timeout', timeout)

    def follow_colored_line(self, timeout=None):
        self.cmd.N = 101
        self.cmd.D1 = 1
        self.cmd.D2 = 1
        self.cmd.execute_command('timeout', timeout)

    def obstacle_avoidance(self):
        self.cmd.N = 101
        self.cmd.D1 = 2
        return self.cmd.execute_command()

    def follow(self):
        self.cmd.N = 101
        self.cmd.D1 = 3
        self.cmd.execute_command()

    def standby_mode(self):
        self.cmd.N = 101
        self.cmd.D1 = 0
        self.cmd.execute_command()

    # Aggiungere eccezione
    def adjust_sensibility(self, sens_value):
        if not sens_value >= 50 and not sens_value <= 1000:
            raise Exception("Error: The value of the sensibility needs to be between 50 and 1000")
        self.cmd.N = 104
        self.cmd.D1 = sens_value
        self.cmd.execute_command('timeout')
