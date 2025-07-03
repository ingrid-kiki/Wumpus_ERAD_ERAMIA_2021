from numpy.core.fromnumeric import size
import AgentInt
import Action
import Location
import Orientation
import LogicRobot

'''
        self.stench = False
        self.breeze = False
        self.glitter = False
        self.bump = False
        self.scream = False
'''
class AgentLogico(AgentInt.AgentInt):
    safe_way = []
    percept_gold = []
    percept_breeze = []
    percept_stench = []
    wumpus_alive = False
    percept_scream_location = None
    has_gold = False
    agente_logico = LogicRobot.MyAI()
    #percept_

    def __init__(self):
        super().__init__()
        self.agente_logico = LogicRobot.MyAI()
        #self.size = size

    def process(self,percept):
        stench = percept[0]
        breeze = percept[1]
        glitter = percept[2]
        bump = percept[3]
        scream = percept[4]
        action = self.agente_logico.getAction(stench, breeze, glitter, bump, scream)
        #action = Action.GOFORWARD
        
        return action

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


