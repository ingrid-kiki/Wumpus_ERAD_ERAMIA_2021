class Location(object):
    """ Location: objeto que representa uma coordenada (x, y) no mapa """

    def __init__(self, x=0, y=0):
        self.x = x  # Coordenada x
        self.y = y  # Coordenada y

    def __eq__(self, other):
        # Verifica se duas localizações são iguais (mesmas coordenadas)
        return self.x == other.x and self.y == other.y

    @staticmethod
    def adjacent(location1, location2):
        """ adjacent: retorna True se as duas localizações são adjacentes """
        x1 = location1.x
        x2 = location2.x
        y1 = location1.y
        y2 = location2.y

        # Verifica se estão lado a lado (horizontal ou vertical)
        if (x1 == x2) and (y1 == (y2 - 1)) or \
           (x1 == x2) and (y1 == (y2 + 1)) or \
           (x1 == (x2 - 1)) and (y1 == y2) or \
           (x1 == (x2 + 1)) and (y1 == y2):
            return True

        return False
    
    @staticmethod
    def isCenter(self, location, size):
        # Retorna True se a localização está no centro (não é canto nem parede)
        if self.isCorner(location, size) or self.isWall(location, size):
            return False
        else:
            return True

    @staticmethod
    def isCorner(location, size):
        # Retorna True se a localização está em um dos cantos do mapa
        x = location.x
        y = location.y
        if (x == size and y == size) or (x == 1 and y == 1):
            return True
        elif x == 1 and y == size:
            return True
        elif y == 1 and x == size:
            return True
        else:
            return False

    @staticmethod
    def isWall(location, size):
        # Retorna True se a localização está em uma das paredes (mas não nos cantos)
        x = location.x
        y = location.y

        if (x > 1 and x < size) and (y == 1 or y == size):
            return True
        elif (y > 1 and y < size) and (x == 1 or x == size):
            return True
        else:
            return False
    
    @staticmethod
    def isOrigem(location):
        # Retorna True se a localização é a origem (1,1)
        x = location.x
        y = location.y

        if x == 1 and y == 1:
            return True
        else:
            return False
    
    @staticmethod
    def adjacentsLocations(self, location, size):
        # Retorna uma lista com as localizações adjacentes válidas
        x = location.x
        y = location.y
        adjacents = []
        if self.isCorner(location, size):
            # Adjacentes para cantos
            if x == 1 and y == 1:
                adjacents.append(Location(x+1, y))
                adjacents.append(Location(x, y+1))
            elif x == 1 and y == size:
                adjacents.append(Location(x+1, y))
                adjacents.append(Location(x, y-1))
            elif x == size and y == size:
                adjacents.append(Location(x-1, y))
                adjacents.append(Location(x, y-1))
            else:
                adjacents.append(Location(x-1, y))
                adjacents.append(Location(x, y+1))
        
        if self.isWall(location, size):
            # Adjacentes para paredes (não cantos)
            if y == 1:
                adjacents.append(Location(x+1, y))
                adjacents.append(Location(x-1, y))
                adjacents.append(Location(x, y+1))
            elif y == size:
                adjacents.append(Location(x+1, y))
                adjacents.append(Location(x-1, y))
                adjacents.append(Location(x, y-1))
            elif x == 1:
                adjacents.append(Location(x, y+1))
                adjacents.append(Location(x, y-1))
                adjacents.append(Location(x+1, y))
            elif x == size:
                adjacents.append(Location(x, y+1))
                adjacents.append(Location(x, y-1))
                adjacents.append(Location(x-1, y))
        
        if self.isCenter():
            # Adjacentes para centro (não canto, não parede)
            adjacents.append(Location(x+1, y))
            adjacents.append(Location(x-1, y))
            adjacents.append(Location(x, y+1))
            adjacents.append(Location(x, y-1))
            
        return adjacents
