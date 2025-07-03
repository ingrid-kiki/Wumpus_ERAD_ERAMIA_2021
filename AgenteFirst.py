import AgentInt
import Action

# Classe que representa um agente controlado pelo usuário (humano)
class AgentFirst(AgentInt.AgentInt):
    def __init__(self):
        # Inicializa a classe base AgentInt
        super().__init__()
    
    # Função principal que processa as percepções do ambiente
    def process(self, percept):
        percept_str = ""
        # Interpreta cada percepção e monta uma string descritiva
        if percept[0] == 1:
            percept_str += "Stench=True,"      # Fedor (Wumpus por perto)
        else:
            percept_str += "Stench=False,"
        if percept[1] == 1:
            percept_str += "Breeze=True,"      # Brisa (Poço por perto)
        else:
            percept_str += "Breeze=False,"
        if percept[2] == 1:
            percept_str += "Glitter=True,"     # Brilho (Ouro na sala)
        else:
            percept_str += "Glitter=False,"
        if percept[3] == 1:
            percept_str += "Bump=True,"        # Colisão (bateu na parede)
        else:
            percept_str += "Bump=False,"
        if percept[4] == 1:
            percept_str += "Scream=True"       # Grito (Wumpus morreu)
        else:
            percept_str += "Scream=False"

        # Exibe as percepções atuais para o usuário
        print("Percepções: " + percept_str)
        print("Escolha para jogar, em seguida <ENTER>:")
        print("8: Avançar" )
        print("4: Virar para Esquerda" )
        print("6: Virar para Direita" )
        print("3: pegar Ouro" )
        print("5: Atirar" )
        print("7: Escalar" )

        # Recebe a ação do usuário via teclado
        pressed = input()

        # Retorna a ação correspondente
        return self.input_key(pressed)

    # Mapeia a tecla pressionada para a ação do agente
    def input_key(self, evento):
        if(evento == '8'):
            return Action.GOFORWARD      # Avançar
        if(evento == '4'):
            return Action.TURNLEFT       # Virar à esquerda
        if(evento == '6'):
            return Action.TURNRIGHT      # Virar à direita
        if(evento == '3'):
            return Action.GRAB           # Pegar ouro
        if(evento == '5'):
            return Action.SHOOT          # Atirar flecha
        if(evento == '7'):
            return Action.CLIMB          # Escalar (sair da caverna)
