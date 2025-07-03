import Action

# Classe base para todos os agentes do ambiente Wumpus
class AgentInt(object):

    def __init__(self):
        # Construtor da classe base, pode ser expandido por subclasses
        pass

    # Método que deve ser implementado pelas subclasses para processar percepções do ambiente
    def process(self, percept) -> Action:
        pass
