import AgentInt
import Action

class AgentFirst(AgentInt.AgentInt):
    def __init__(self):
        super().__init__()
    
    def process(self,percept):
        percept_str = ""
        if percept[0] == 1:
            percept_str += "Stench=True,"
        else:
            percept_str += "Stench=False,"
        if percept[1] == 1:
            percept_str += "Breeze=True,"
        else:
            percept_str += "Breeze=False,"
        if percept[2] == 1:
            percept_str += "Glitter=True,"
        else:
            percept_str += "Glitter=False,"
        if percept[3] == 1:
            percept_str += "Bump=True,"
        else:
            percept_str += "Bump=False,"
        if percept[4] == 1:
            percept_str += "Scream=True"
        else:
            percept_str += "Scream=False"

        print("Percepções: " + percept_str)
        print("Escolha para jogar, em seguida <ENTER>:")
        print("8: Avançar" )
        print("4: Virar para Esquerda" )
        print("6: Virar para Direita" )
        print("3: pegar Ouro" )
        print("5: Atirar" )
        print("7: Escalar" )

        pressed = input()

        return self.input_key(pressed)


    def input_key(self,evento):
    
        if(evento == '8'):
            return Action.GOFORWARD
        if(evento == '4'):
            return Action.TURNLEFT
        if(evento == '6'):
            return Action.TURNRIGHT
        if(evento == '3'):
            return Action.GRAB
        if(evento == '5'):
            return Action.SHOOT
        if(evento == '7'):
            return Action.CLIMB
