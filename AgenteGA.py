from numpy.core.fromnumeric import size
import AgentInt
import Action

# Classe que representa um agente controlado por Algoritmo Genético
class AgentGA(AgentInt.AgentInt):
    AG_moves = []        # Lista de movimentos definidos pelo cromossomo
    i = 0                # Índice do movimento atual
    max_movements = 0    # Número máximo de movimentos permitidos
    size_cromo = 0       # Tamanho do cromossomo

    def __init__(self, list_action, max_movements, size_cromo):
        super().__init__()
        self.AG_moves = list_action          # Sequência de ações do agente (cromossomo)
        self.i = 0                          # Inicializa o índice do movimento
        self.max_movements = max_movements  # Define o número máximo de movimentos
        self.size_cromo = size_cromo        # Define o tamanho do cromossomo

    # Função principal que processa as percepções do ambiente
    def process(self, percept):
        # Se ainda não atingiu o limite de movimentos, executa o próximo movimento
        if self.max_movements > self.i + 1:
            movement = self.AG_moves[self.i]  # Seleciona o movimento atual
            self.i = self.i + 1               # Avança para o próximo movimento
        else:
            movement = 7                      # Caso contrário, executa a ação de término (END)
        
        return self.input_key(movement)       # Retorna a ação correspondente

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
