from numpy.core.fromnumeric import size
import AgentInt
import Action

class AgentGA(AgentInt.AgentInt):
    AG_moves = []
    i = 0
    max_movements = 0
    size_cromo = 0
    def __init__(self,list_action,max_movements,size_cromo):
        super().__init__()
        self.AG_moves = list_action
        self.i = 0
        self.max_movements = max_movements
        self.size_cromo = size_cromo

    def process(self,percept):
        if self.max_movements > self.i + 1:
            movement = self.AG_moves[self.i]
            self.i = self.i + 1
        else:
            movement = 7
        
        return self.input_key(movement)


    def input_key(self,evento):
    
        if(evento == 0):
            return Action.GOFORWARD
        if(evento == 1):
            return Action.TURNLEFT
        if(evento == 2):
            return Action.TURNRIGHT
        if(evento == 3):
            return Action.GRAB
        if(evento == 4):
            return Action.SHOOT
        if(evento == 5):
            return Action.CLIMB
        if(evento == 6):
            return Action.UNK
        if(evento == 7):
            return Action.END