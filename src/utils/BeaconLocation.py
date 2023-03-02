class BeaconLocation:
    def __init__(self, name, x, y, z):
        self.name = name
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f'Location {self.name} : ({self.x}, {self.y}, {self.z})'
