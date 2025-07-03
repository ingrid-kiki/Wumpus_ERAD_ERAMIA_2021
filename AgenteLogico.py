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
# Classe que representa um agente lógico (baseado em regras/lógica)
class AgentLogico(AgentInt.AgentInt):
    safe_way = []                  # Caminhos considerados seguros
    percept_gold = []              # Percepções de ouro
    percept_breeze = []            # Percepções de brisa
    percept_stench = []            # Percepções de fedor
    wumpus_alive = False           # Estado do Wumpus (vivo/morto)
    percept_scream_location = None # Localização onde ouviu o grito
    has_gold = False               # Se o agente já pegou o ouro
    agente_logico = LogicRobot.MyAI() # Instância do agente lógico

    def __init__(self):
        super().__init__()
        self.agente_logico = LogicRobot.MyAI() # Inicializa o agente lógico

    # Função principal que processa as percepções do ambiente
    def process(self, percept):
        stench = percept[0]   # Fedor (Wumpus por perto)
        breeze = percept[1]   # Brisa (Poço por perto)
        glitter = percept[2]  # Brilho (Ouro na sala)
        bump = percept[3]     # Colisão (bateu na parede)
        scream = percept[4]   # Grito (Wumpus morreu)
        # Obtém a ação do agente lógico baseado nas percepções
        action = self.agente_logico.getAction(stench, breeze, glitter, bump, scream)
        # Retorna a ação escolhida
        return action

    # Mapeia o valor do movimento para a ação do agente
    def input_key(self, evento):
        if(evento == 0):
            return Action.GOFORWARD   # Avançar
        if(evento == 1):
            return Action.TURNLEFT    # Virar à esquerda
        if(evento == 2):
            return Action.TURNRIGHT   # Virar à direita
        if(evento == 3):
            return Action.GRAB        # Pegar ouro
        if(evento == 4):
            return Action.SHOOT       # Atirar flecha
        if(evento == 5):
            return Action.CLIMB       # Escalar (sair da caverna)
        if(evento == 6):
            return Action.UNK         # Ação desconhecida
        if(evento == 7):
            return Action.END         # Finalizar execução


