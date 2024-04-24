class UltrasonicUnit:
    def __init__(self, command) -> None:
        self.cmd = command
    
    # Return the value of the ultrasonic sensor
    def distance(self):
        self.cmd.D1 = 2
        return self.cmd.execute_command()
    
    # Return true if an obstacle is detected
    def obstacle(self, distance):
        self.cmd.D1 = 2
        detected_disance = int(self.cmd.execute_command())
        print(f'Detected distance: {detected_disance}')
        if detected_disance <= distance:
            return True
        return False
    
    # Return the motion of the car in (x,y,z) axis
    def motion(self):
        self.cmd.N = 6
        return self.cmd.execute_command()
    
    def light_refraction(self, sensor):
        self.cmd.N = 22
        if sensor == 'L':
            self.cmd.D1 = 0
        if sensor == 'M':
            self.cmd.D1 = 1
        if sensor == 'R':
            self.cmd.D1 = 2
        try:
            return int(self.cmd.execute_command())
        except:
            return 0
