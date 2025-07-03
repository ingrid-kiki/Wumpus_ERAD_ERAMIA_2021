import numpy
from numpy import random
import WumpsimAG
import numpy as np
import time

# Função para calcular o fitness de cada indivíduo da população
def cal_pop_fitness(pop, print_world, size_cromo, wumpus_world, seed=50):
    # Calcula o valor de fitness de cada solução na população atual.
    current_state = []
    fitness = []
    for i, cromo in enumerate(pop):
        # Executa o simulador com o cromossomo atual e obtém os resultados
        avgscore, totalscore, has_gold, death_wumpus, win, alive = WumpsimAG.run(
            cromo, print_world=print_world, size_cromo=size_cromo, seed=seed, world_generated=wumpus_world
        )
        fitness.append(-1 * totalscore)  # Fitness negativo do score total (minimização)
        current_state.append([has_gold, death_wumpus, win, alive])  # Estado do agente
        random.seed(int(np.ceil(time.time())))  # Atualiza a seed aleatória
    return fitness, current_state

# Seleção por torneio (tournament selection)
def selection(pop, scores, k=3):
    # Seleciona um indivíduo da população usando torneio de tamanho k
    selection_ix = np.random.randint(len(pop))  # Seleção inicial aleatória
    for ix in np.random.randint(0, len(pop), k-1):
        # Se encontrar um indivíduo com score melhor, seleciona ele
        if scores[ix] < scores[selection_ix]:
            selection_ix = ix
    return pop[selection_ix]

# Elitismo: seleciona os melhores indivíduos para a próxima geração
def elitism(pop, scores, ratio):
    size = int(np.ceil(len(pop) * ratio))  # Calcula o número de elites
    pop = np.array(pop)
    elit_pop = pop[np.argsort(scores)]     # Ordena população pelo score
    elit_pop = elit_pop[:size, :]          # Seleciona os melhores
    return list(elit_pop), size

# Cruzamento (crossover) de dois pais para gerar dois filhos
def crossover(p1, p2, r_cross):
    # Os filhos são cópias dos pais por padrão
    c1, c2 = p1.copy(), p2.copy()
    # Verifica se ocorre recombinação
    if np.random.rand() < r_cross:
        # Seleciona ponto de crossover (não nas extremidades)
        pt = np.random.randint(1, len(p1) - 2)
        # Realiza o crossover
        c1 = list(p1[:pt]) + list(p2[pt:])
        c2 = list(p2[:pt]) + list(p1[pt:])
    return [c1, c2]

# Gera a próxima geração a partir dos selecionados
def next_generation(selected, n_pop, r_cross, r_mut, min, max):
    children = list()
    for i in range(0, n_pop, 2):
        # Seleciona pares de pais
        p1, p2 = selected[i], selected[i+1]
        # Cruzamento e mutação
        for c in crossover(p1, p2, r_cross):
            # Mutação
            mutation(c, r_mut, min, max)
            # Adiciona filho à próxima geração
            children.append(c)
    return children

# Operador de mutação
def mutation(bitstring, r_mut, min, max):
    for i in range(len(bitstring)):
        # Verifica se ocorre mutação
        if np.random.rand() < r_mut:
            # Altera o gene para um valor aleatório dentro do intervalo permitido
            bitstring[i] = np.random.randint(low=min, high=max+1)


