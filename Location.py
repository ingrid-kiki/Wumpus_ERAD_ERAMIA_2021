class Location(object):
    """ Location: location object that holds an x, y coordinate in the map """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @staticmethod
    def adjacent(location1, location2):
        """ adjacent: returns true if the two locations and next to each other """

        x1 = location1.x
        x2 = location2.x
        y1 = location1.y
        y2 = location2.y

        if (x1 == x2) and (y1 == (y2 - 1)) or \
           (x1 == x2) and (y1 == (y2 + 1)) or \
           (x1 == (x2 - 1)) and (y1 == y2) or \
           (x1 == (x2 + 1)) and (y1 == y2):
            return True

        return False
    
    @staticmethod
    def isCenter(self,location,size):
        if self.isCorner(location,size) or self.isWall(location,size):
            return False
        else:
            return True

    @staticmethod
    def isCorner(location,size):
        x = location.x
        y = location.y
        if (x==size and y==size) or (x==1 and y==1):
            return True
        elif x==1 and y==size:
            return True
        elif y==1 and x == size:
            return True
        else:
            return False

    @staticmethod
    def isWall(location,size):
        x = location.x
        y = location.y

        if (x>1 and x<size) and (y == 1 or y == size):
            return True
        elif (y>1 and y<size) and (x == 1 or x == size):
            return True
        else:
            return False
    
    @staticmethod
    def isOrigem(location):
        x = location.x
        y = location.y

        if x==1 and y==1:
            return True
        else:
            return False
    
    @staticmethod
    def adjacentsLocations(self,location,size):
        x = location.x
        y = location.y
        adjacents = []
        if self.isCorner(location,size):
            if x == 1 and y == 1:
                adjacents.append(Location(x+1,y))
                adjacents.append(Location(x,y+1))
            elif x==1 and y == size:
                adjacents.append(Location(x+1,y))
                adjacents.append(Location(x,y-1))
            elif x==size and y == size:
                adjacents.append(Location(x-1,y))
                adjacents.append(Location(x,y-1))
            else:
                adjacents.append(Location(x-1,y))
                adjacents.append(Location(x,y+1))
        
        if self.isWall(location,size):
            if y == 1:
                adjacents.append(Location(x+1,y))
                adjacents.append(Location(x-1,y))
                adjacents.append(Location(x,y+1))
            elif y == size:
                adjacents.append(Location(x+1,y))
                adjacents.append(Location(x-1,y))
                adjacents.append(Location(x,y-1))
            elif x == 1:
                adjacents.append(Location(x,y+1))
                adjacents.append(Location(x,y-1))
                adjacents.append(Location(x+1,y))
            elif x == size:
                adjacents.append(Location(x,y+1))
                adjacents.append(Location(x,y-1))
                adjacents.append(Location(x-1,y))
        
        if self.isCenter():
            adjacents.append(Location(x+1,y))
            adjacents.append(Location(x-1,y))
            adjacents.append(Location(x,y+1))
            adjacents.append(Location(x,y-1))
            
        return adjacents