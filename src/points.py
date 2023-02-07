def getAllPoints():
    points = []
    with open('CARTO-LAB.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            name, x, y, z = line.split(',')
            points.append(Point(name, x, y, z))
    return points

def get_used_points(dict_elements):
    used_points = []
    for point in getAllPoints():
        if point.name in dict_elements:
            used_points.append(point)
    return used_points

class Point:
    def __init__(self, name, x, y, z):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
    def myprint(self):
        return (f'{self.name}')