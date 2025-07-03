# https://github.com/erikphillips/wumpus_world
#
# Simulador do Mundo de Wumpus - Versão Reativa
# Este arquivo implementa o ambiente, as percepções, o estado do mundo e a interface com o agente.

from argparse import Action
import os
from Action import *
from Orientation import *
import PyAgent
import random
import sys
import time

# Versão do simulador
WUMPSIM_VERSION = "v1.2"

# Tamanho do mundo (quadrado)
WORLD_SIZE = 8

# Probabilidade de um poço estar em uma posição
PIT_PROBABILITY = 0.2

# Número máximo de movimentos por jogo
MAX_MOVES_PER_GAME = 200

# Classe que representa as percepções do agente (fedor, brisa, brilho, batida, grito)
class Percept(object):
    def __init__(self):
        """ Inicializa todas as percepções como falsas """
        self.stench = False
        self.breeze = False
        self.glitter = False
        self.bump = False
        self.scream = False

    def initialize(self):
        """ Reseta todas as percepções para o valor padrão (False) """
        self.stench = False
        self.breeze = False
        self.glitter = False
        self.bump = False
        self.scream = False

# Classe que representa o estado do mundo (posições do agente, wumpus, ouro e poços)
class State(object):
    """ Guarda as informações do estado atual do jogo """

    def __init__(self, file_information):
        """
        Cria um novo estado para o mundo Wumpus.
        Se não houver arquivo, gera posições aleatórias para wumpus, ouro e poços.
        """
        if file_information is None:
            self.wumpus_location = self._get_wumpus_location()
            self.gold_location = self._get_gold_location()
            # Garante que ouro e wumpus não estejam na mesma posição
            while self.gold_location.__eq__(self.wumpus_location):
                self.gold_location = self._get_gold_location()
            # Gera poços e garante que não coincidam com ouro ou wumpus
            self.pit_locations = self._get_pit_locations()
            teste = True
            while teste:
                teste = False
                self.pit_locations = self._get_pit_locations()
                for location in self.pit_locations:
                    if location.__eq__(self.wumpus_location) or location.__eq__(self.gold_location):
                        teste = True
                        self.pit_locations = None
        else:
            # Usa informações de arquivo, se fornecidas
            self.wumpus_location = file_information.wumpus_location
            self.gold_location = file_information.gold_location
            self.pit_locations = file_information.pit_locations

        # Inicializa estado do agente
        self.agent_location = Location(1, 1)
        self.agent_orientation = RIGHT
        self.agent_alive = True
        self.agent_has_arrow = True
        self.agent_has_gold = False
        self.agent_in_cave = True
        self.wumpus_alive = True

    def initialize(self):
        """ Reseta o estado do agente para o início de uma nova tentativa """
        self.agent_location = Location(1, 1)
        self.agent_orientation = RIGHT
        self.agent_alive = True
        self.agent_has_arrow = True
        self.agent_has_gold = False
        self.agent_in_cave = True
        self.wumpus_alive = True

    def _get_gold_location(self):
        """ Retorna uma localização aleatória para o ouro (exceto (1,1)) """
        x, y = self._get_random_location()
        return Location(x, y)

    def _get_wumpus_location(self):
        """ Retorna uma localização aleatória para o wumpus (exceto (1,1)) """
        x, y = self._get_random_location()
        return Location(x, y)

    @staticmethod
    def _get_random_location():
        """ Retorna uma localização aleatória que não seja (1,1) """
        x = 1
        y = 1
        while (x == 1) and (y == 1):
            x = random.randint(1, WORLD_SIZE)
            y = random.randint(1, WORLD_SIZE)
        return x, y

    @staticmethod
    def _get_pit_locations():
        """ Retorna uma lista de localizações de poços, baseando-se na probabilidade """
        locations = []
        for x in range(1, WORLD_SIZE + 1):
            for y in range(1, WORLD_SIZE + 1):
                if (x != 1) or (y != 1):
                    if (random.randint(0, 1000 - 1)) < (PIT_PROBABILITY * 1000):
                        locations.append(Location(x, y))
        return locations

# Classe que representa uma posição no mapa (x, y)
class Location(object):
    """ Objeto de localização (x, y) """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @staticmethod
    def adjacent(location1, location2):
        """ Retorna True se as duas localizações são adjacentes (horizontal ou vertical) """
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

    # Métodos auxiliares para verificar se a posição é centro, canto, parede ou origem
    @staticmethod
    def isCenter(self,location,size):
        # Retorna True se não for canto nem parede
        if self.isCorner(location,size) or self.isWall(location,size):
            return False
        else:
            return True

    @staticmethod
    def isCorner(location,size):
        # Retorna True se a posição for um dos cantos do mapa
        x = location.x
        y = location.y
        if x == y:
            return True
        elif x==1 & y==size:
            return True
        elif y==1 & x == size:
            return True
        else:
            return False

    @staticmethod
    def isWall(location,size):
        # Retorna True se a posição for uma parede (mas não canto)
        x = location.x
        y = location.y
        if (x>1 and x<size) and (y == 1 or y == size):
            return True
        elif (y>1 and y<size) and (x == 1 or x == size):
            return True
        else:
            return False

    @staticmethod
    def isOrigem(location,size):
        # Retorna True se for a origem (1,1)
        x = location.x
        y = location.y
        if x==1 and y==1:
            return True
        else:
            return False

    @staticmethod
    def adjacentsLocations(self,location,size):
        # Retorna lista de localizações adjacentes válidas
        x = location.x
        y = location.y
        adjacents = []
        # Adiciona adjacentes conforme tipo de posição (canto, parede, centro)
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

# Classe principal do mundo Wumpus
class WumpusWorld(object):
    def __init__(self, file_information=None):
        """
        Cria um novo mundo Wumpus, posicionando wumpus, ouro e poços.
        Atualiza as percepções iniciais do agente.
        """
        self.num_actions = 0
        self.current_state = State(file_information=file_information)
        self.current_percept = Percept()

        # Atualiza percepções iniciais do agente
        if Location.adjacent(self.current_state.agent_location, self.current_state.wumpus_location) or \
           (self.current_state.agent_location == self.current_state.wumpus_location):
            self.current_percept.stench = True
        for pit in self.current_state.pit_locations:
            if Location.adjacent(self.current_state.agent_location, pit):
                self.current_percept.breeze = True
        if self.current_state.gold_location.x == 1 and self.current_state.gold_location.y == 1:
            self.current_percept.glitter = True

    def initialize(self):
        """ Reseta o mundo e as percepções para uma nova tentativa """
        self.num_actions = 0
        self.current_state.initialize()
        self.current_percept.initialize()
        # Atualiza percepções iniciais novamente
        if Location.adjacent(self.current_state.agent_location, self.current_state.wumpus_location) or \
           (self.current_state.agent_location == self.current_state.wumpus_location):
            self.current_percept.stench = True
        for pit in self.current_state.pit_locations:
            if Location.adjacent(self.current_state.agent_location, pit):
                self.current_percept.breeze = True
        if self.current_state.gold_location.x == 1 and self.current_state.gold_location.y == 1:
            self.current_percept.glitter = True

    def get_percept(self):
        """ Retorna as percepções atuais do agente """
        return self.current_percept

    def execute_action(self, action):
        """
        Executa a ação fornecida pelo agente, atualizando a localização e as percepções.
        Controla movimentação, giro, pegar ouro, atirar flecha e sair da caverna.
        """
        if action != UNK:
            self.num_actions += 1
            self.current_percept.bump = False
            self.current_percept.scream = False
            # Movimentação do agente
            if action == GOFORWARD:
                # Atualiza posição do agente conforme orientação
                if self.current_state.agent_orientation == RIGHT:
                    if self.current_state.agent_location.x < WORLD_SIZE:
                        self.current_state.agent_location.x += 1
                    else:
                        self.current_percept.bump = True
                elif self.current_state.agent_orientation == UP:
                    if self.current_state.agent_location.y < WORLD_SIZE:
                        self.current_state.agent_location.y += 1
                    else:
                        self.current_percept.bump = True
                elif self.current_state.agent_orientation == LEFT:
                    if self.current_state.agent_location.x > 1:
                        self.current_state.agent_location.x -= 1
                    else:
                        self.current_percept.bump = True
                elif self.current_state.agent_orientation == DOWN:
                    if self.current_state.agent_location.y > 1:
                        self.current_state.agent_location.y -= 1
                    else:
                        self.current_percept.bump = True
                # Atualiza percepções após movimento
                self.current_percept.glitter = False
                if (not self.current_state.agent_has_gold) and \
                        (self.current_state.agent_location == self.current_state.gold_location):
                    self.current_percept.glitter = True
                self.current_percept.stench = False
                if Location.adjacent(self.current_state.agent_location, self.current_state.wumpus_location) or \
                        (self.current_state.agent_location == self.current_state.wumpus_location):
                    self.current_percept.stench = True
                self.current_percept.breeze = False
                for pit in self.current_state.pit_locations:
                    if Location.adjacent(self.current_state.agent_location, pit):
                        self.current_percept.breeze = True
                    elif self.current_state.agent_location == pit:
                        self.current_state.agent_alive = False
                # Verifica se morreu pelo wumpus
                if self.current_state.wumpus_alive and \
                        (self.current_state.agent_location == self.current_state.wumpus_location):
                    self.current_state.agent_alive = False
            # Gira o agente para a esquerda
            if action == TURNLEFT:
                if self.current_state.agent_orientation == RIGHT:
                    self.current_state.agent_orientation = UP
                elif self.current_state.agent_orientation == UP:
                    self.current_state.agent_orientation = LEFT
                elif self.current_state.agent_orientation == LEFT:
                    self.current_state.agent_orientation = DOWN
                elif self.current_state.agent_orientation == DOWN:
                    self.current_state.agent_orientation = RIGHT
            # Gira o agente para a direita
            if action == TURNRIGHT:
                if self.current_state.agent_orientation == RIGHT:
                    self.current_state.agent_orientation = DOWN
                elif self.current_state.agent_orientation == UP:
                    self.current_state.agent_orientation = RIGHT
                elif self.current_state.agent_orientation == LEFT:
                    self.current_state.agent_orientation = UP
                elif self.current_state.agent_orientation == DOWN:
                    self.current_state.agent_orientation = LEFT
            # Pega o ouro
            if action == GRAB:
                if not self.current_state.agent_has_gold and \
                        (self.current_state.agent_location == self.current_state.gold_location):
                    self.current_state.agent_has_gold = True
                    self.current_percept.glitter = False
            # Atira a flecha
            if action == SHOOT:
                if self.current_state.agent_has_arrow:
                    self.current_state.agent_has_arrow = False
                    if self.current_state.wumpus_alive:
                        # Verifica se acertou o wumpus
                        if (((self.current_state.agent_orientation == RIGHT) and
                            (self.current_state.agent_location.x < self.current_state.wumpus_location.x) and
                            (self.current_state.agent_location.y == self.current_state.wumpus_location.y)) or
                            ((self.current_state.agent_orientation == UP) and
                            (self.current_state.agent_location.x == self.current_state.wumpus_location.x) and
                            (self.current_state.agent_location.y < self.current_state.wumpus_location.y)) or
                            ((self.current_state.agent_orientation == LEFT) and
                            (self.current_state.agent_location.x > self.current_state.wumpus_location.x) and
                            (self.current_state.agent_location.y == self.current_state.wumpus_location.y)) or
                            ((self.current_state.agent_orientation == DOWN) and
                            (self.current_state.agent_location.x == self.current_state.wumpus_location.x) and
                            (self.current_state.agent_location.y > self.current_state.wumpus_location.y))):
                            self.current_state.wumpus_alive = False
                            self.current_percept.scream = True
            # Sair da caverna
            if action == CLIMB:
                if self.current_state.agent_location.x == 1 and self.current_state.agent_location.y == 1:
                    self.current_state.agent_in_cave = False
                    self.current_percept.stench = False
                    self.current_percept.breeze = False
                    self.current_percept.glitter = False

    def game_over(self):
        """ Retorna True se o jogo acabou (agente saiu ou morreu) """
        return not self.current_state.agent_in_cave or not self.current_state.agent_alive

    def get_current_state(self):
        """ Retorna informações do estado final do agente (ouro, wumpus, vitória, vivo) """
        death_wumpus = 1 - self.current_state.wumpus_alive
        has_gold = int(self.current_state.agent_has_gold)
        win = 0
        alive = self.current_state.agent_alive
        if self.current_state.agent_has_gold and not self.current_state.agent_in_cave:
            win = 1
        return has_gold,death_wumpus,win,alive

    def get_score(self):
        """
        Calcula e retorna a pontuação do agente:
        -1 por ação, -10 por atirar flecha, +1000 por sair com ouro, -1000 por morrer, +100 se matar o wumpus
        """
        score = 0
        score -= self.num_actions
        if not self.current_state.agent_has_arrow:
            score -= 9
        if self.current_state.agent_has_gold and not self.current_state.agent_in_cave:
            score += 1000
        if not self.current_state.agent_alive:
            score -= 1000
        if not self.current_state.wumpus_alive:
            score +=100
        return score

    def print_world(self):
        """
        Imprime o estado atual do mundo Wumpus no terminal.
        Mostra o mapa, percepções e status do agente.
        """
        os.system('cls')
        print("World size = {}x{}".format(WORLD_SIZE, WORLD_SIZE))
        # Imprime o mapa linha por linha
        out = "+"
        for x in range(1, WORLD_SIZE + 1):
            out += "---+"
        print(out)
        for y in range(WORLD_SIZE, 0, -1):  # do 'fundo' para cima
            # Primeira linha: wumpus, ouro, poço
            out = "|"
            for x in range(1, WORLD_SIZE + 1):
                if self.current_state.wumpus_location == Location(x, y):
                    if self.current_state.wumpus_alive:
                        out += "W"
                    else:
                        out += "x"
                else:
                    out += " "
                if not self.current_state.agent_has_gold and self.current_state.gold_location == Location(x, y):
                    out += "G"
                else:
                    out += " "
                _has_pit = False
                for pit in self.current_state.pit_locations:
                    if pit == Location(x, y):
                        _has_pit = True
                if _has_pit:
                    out += "P"
                else:
                    out += " "
                out += "|"
            print(out)
            # Segunda linha: agente
            out = "|"
            for x in range(1, WORLD_SIZE + 1):
                if self.current_state.agent_alive and self.current_state.agent_location == Location(x, y):
                    if self.current_state.agent_orientation == RIGHT:
                        out += " A>|"
                    elif self.current_state.agent_orientation == UP:
                        out += " A^|"
                    elif self.current_state.agent_orientation == LEFT:
                        out += " A<|"
                    else:
                        out += " Av|"
                else:
                    out += "   |"
            print(out)
            out = "+"
            for x in range(1, WORLD_SIZE + 1):
                out += "---+"
            print(out)
        # Imprime percepções e status do agente
        print("Current percept = [stench={},breeze={},glitter={},bump={},scream={}]".format(
            self.current_percept.stench,
            self.current_percept.breeze,
            self.current_percept.glitter,
            self.current_percept.bump,
            self.current_percept.scream))
        print("Agent has gold = {}, agent has arrow = {}".format(
            self.current_state.agent_has_gold,
            self.current_state.agent_has_arrow))
        print("Current score = {}".format(self.get_score()))
        print()

# Classe para ler informações do mundo a partir de arquivo
class WumpusWorldFileInformation(object):
    def __init__(self, filename):
        self.world_size = WORLD_SIZE
        self.wumpus_location = None
        self.gold_location = None
        self.pit_locations = []
        with open(filename, "r") as infile:
            lines = infile.readlines()
            if len(lines) < 3:  # precisa de pelo menos 3 linhas: size, wumpus, gold
                print("Invalid world file; required: size, wumpus, and gold locations.")
                sys.exit(1)
            self._process_size(lines[0])
            self._process_wumpus(lines[1])
            self._process_gold(lines[2])
            if len(lines) > 3:  # processa poços se houver mais linhas
                self._process_pits(lines[3:])

    def _process_size(self, line):
        global WORLD_SIZE
        size_tokens = line.strip().split(" ")
        if len(size_tokens) != 2 or size_tokens[0] != "size":
            print("Incorrect token in world file '{}', expected 'size'".format(size_tokens[0]))
            sys.exit(1)
        self.world_size = int(size_tokens[1])
        if self.world_size < 2:
            print("Invalid world size, size < 2.")
            sys.exit(1)
        WORLD_SIZE = self.world_size  # atualiza tamanho global

    def _process_wumpus(self, line):
        tokens = line.strip().split(" ")
        if len(tokens) != 3 or tokens[0] != "wumpus":
            print("Incorrect token in world file '{}', expected 'wumpus'".format(tokens[0]))
            sys.exit(1)
        loc_x = int(tokens[1])
        loc_y = int(tokens[2])
        if (1 > loc_x > self.world_size) or (1 > loc_y > self.world_size) or (loc_x == 1 and loc_y == 1):
            print("Bad wumpus location in world file for location ({}, {}).".format(loc_x, loc_y))
            sys.exit(1)
        self.wumpus_location = Location(loc_x, loc_y)

    def _process_gold(self, line):
        tokens = line.strip().split(" ")
        if len(tokens) != 3 or tokens[0] != "gold":
            print("Incorrect token in world file '{}', expected 'gold'".format(tokens[0]))
            sys.exit(1)
        loc_x = int(tokens[1])
        loc_y = int(tokens[2])
        if (1 > loc_x > self.world_size) or (1 > loc_y > self.world_size) or (loc_x == 1 and loc_y == 1):
            print("Bad gold location in world file for location ({}, {}).".format(loc_x, loc_y))
            sys.exit(1)
        self.gold_location = Location(loc_x, loc_y)

    def _process_pits(self, lines):
        for line in lines:
            tokens = line.strip().split(" ")
            if len(tokens) != 3 or tokens[0] != "pit":
                print("Incorrect token in world file '{}', expected 'pit'".format(tokens[0]))
                sys.exit(1)
            loc_x = int(tokens[1])
            loc_y = int(tokens[2])
            if (1 > loc_x > self.world_size) or (1 > loc_y > self.world_size) or (loc_x == 1 and loc_y == 1):
                print("Bad pit location in world file for location ({}, {}).".format(loc_x, loc_y))
                sys.exit(1)
            self.pit_locations.append(Location(loc_x, loc_y))

# Classe para interface com o agente
class Agent(object):
    @staticmethod
    def construct(agente = 2,aglist=None,size_cromo=None):
        # Inicializa o agente chamando o construtor do PyAgent
        PyAgent.PyAgent_Constructor(agente,aglist,MAX_MOVES_PER_GAME,size_cromo=size_cromo)

    @staticmethod
    def initialize():
        # Inicializa o agente para uma nova tentativa
        PyAgent.PyAgent_Initialize()

    @staticmethod
    def process(percept):
        # Processa as percepções e retorna a ação do agente
        return PyAgent.PyAgent_Process(percept.stench, percept.breeze, percept.glitter, percept.bump, percept.scream)

    @staticmethod
    def game_over(score):
        # Informa ao agente que o jogo terminou e passa a pontuação final
        PyAgent.PyAgent_GameOver(score)

    @staticmethod
    def destructor():
        # Chama o destrutor do agente
        PyAgent.PyAgent_Destructor()

# Função utilitária para converter ação em string
def action_to_string(action):
    """ Retorna uma string correspondente à ação """
    if action == GOFORWARD:
        return "GOFORWARD"
    if action == TURNRIGHT:
        return "TURNRIGHT"
    if action == TURNLEFT:
        return "TURNLEFT"
    if action == SHOOT:
        return "SHOOT"
    if action == GRAB:
        return "GRAB"
    if action == CLIMB:
        return "CLIMB"
    return "UNKNOWN ACTION"

# Função principal para rodar o simulador
def run(print_world=False,seed=50):
    # Inicializa variáveis de controle
    AG_moves = None
    size_cromo = None
    total_score = 0
    tries = None
    trials = None
    world = None
    agente = 2
    has_gold = 0
    death_wumpus = 0
    win = 0

    if tries is None:
        tries = 1
    if trials is None:
        trials = 1
    if agente is None:
        agente = 1

    # Define a semente do gerador aleatório
    random.seed(seed)

    for trials in range(1, trials + 1):
        file_information = None
        if world is not None:
            file_information = WumpusWorldFileInformation(world)
        wumpus_world = WumpusWorld(file_information=file_information)  # Cria novo mundo
        Agent.construct(agente=agente,aglist=AG_moves,size_cromo=size_cromo)  # Inicializa agente

        trial_score = 0

        for tries in range(1, tries + 1):
            wumpus_world.initialize()  # Reseta mundo
            Agent.initialize()         # Reseta agente

            num_moves = 0

            if print_world:
                print("Trial {}, Try {} begin".format(trials, tries))
                print()
            action = UNK
            while (not wumpus_world.game_over()) and (num_moves < MAX_MOVES_PER_GAME) and action != END:
                if print_world:
                    time.sleep(0.5)
                    wumpus_world.print_world()
                percept = wumpus_world.get_percept()  # Obtém percepções
                action = Agent.process(percept)        # Agente decide ação
                if print_world:
                    print("Action = {}".format(action_to_string(action)))
                    print()
                wumpus_world.execute_action(action)    # Executa ação
                num_moves += 1

            score = wumpus_world.get_score()  # Pontuação final
            Agent.game_over(score)            # Informa agente do fim do jogo
            trial_score += score
            if print_world:
                print("Trial {}, Try {} complete: score = {}\n".format(trials, tries, score))

        Agent.destructor()  # Finaliza agente ao fim do trial
        average_score = trial_score / tries
        total_score += trial_score / num_moves
        has_gold,death_wumpus,win,alive = wumpus_world.get_current_state()

        if print_world:
            # Exibe o resultado do trial atual: média e pontuação total
            print("Trial {} complete: Average score for trial = {}, total score for trial = {}\n".format(
                trials, average_score, trial_score))

    # Calcula a média dos scores de todos os trials realizados
    average_score = total_score / (trials * tries)

    if print_world:
        # Exibe o resultado final após todas as execuções (média geral e total)
        print("All trials completed: Average score for all trials = {}, " \
              "Total score for all trials = {}".format(average_score, total_score))
        print("Thanks for playing!")

    # Retorna métricas do desempenho do agente:
    # - average_score: média dos scores por ação em todas as execuções
    # - total_score: soma dos scores normalizados por número de movimentos
    # - has_gold: 1 se o agente pegou o ouro, 0 caso contrário
    # - death_wumpus: 1 se o Wumpus morreu, 0 caso contrário
    # - win: 1 se o agente venceu (pegou o ouro e saiu), 0 caso contrário
    # - alive: 1 se o agente terminou vivo, 0 caso contrário
    return average_score, total_score, has_gold, death_wumpus, win, int(alive)
