import numpy as np
from numpy import random
import ga  # Módulo com funções do algoritmo genético
import time
import pickle
from WumpsimAG import WumpusWorld
import winsound

# Parâmetros do ambiente e do algoritmo genético
size_world = 6           # Tamanho do mundo Wumpus (6x6)
size_chromo = 200        # Tamanho do cromossomo (quantidade de ações)
size_pop = 100           # Tamanho da população
num_parents_mating = 2   # Número de pais para crossover
num_generations = 100    # Número de gerações
crossover_probability = 0.5
mutation_probability = 0.15
tournament_number = 3    # Número de indivíduos no torneio de seleção
elit_ratio = 0.02        # Proporção de elitismo
min = 0                  # Valor mínimo de gene (ação)
max = 6                  # Valor máximo de gene (ação)

# Sinal sonoro para indicar início da execução
winsound.Beep(550,1000)

# Parâmetros de execução dos testes
seed = 50
tests = 10               # Quantidade de testes por mundo
worlds = 5               # Quantidade de mundos diferentes
seeds = [43,44,45,46,50] # Sementes para geração dos mundos

# Dicionário para armazenar resultados dos testes
results = {'fitness':[],'test':[],'world':[],'gold':[],'death_wumpus':[],'win':[],'alive':[],'cromo':[]}

inicio = time.time()     # Marca o tempo inicial da execução

# Loop principal: para cada mundo
for world in range(worlds):
    wumpus_world = None  # Pode ser usado para passar um mundo fixo, aqui está como None (aleatório)
    # Para cada teste dentro do mundo
    for test in range(tests):
        best_outputs = []        # Guarda o melhor fitness de cada geração
        best_cromo = []          # Guarda o melhor cromossomo de cada geração
        best_fitness_all = []    # Guarda o melhor fitness acumulado
        best_current_state = []  # Guarda o estado do agente para o melhor cromossomo
        random.seed(world + test + size_world)  # Semente para reprodutibilidade
        # Inicializa população aleatória de cromossomos (ações)
        new_population = np.random.randint(low=min, high=max+1, size=(size_pop,size_chromo))
        # Evolução por gerações
        for generation in range(num_generations):
            # Avalia fitness de cada cromossomo
            fitness,current_state = ga.cal_pop_fitness(new_population,print_world=False,size_cromo=size_chromo,wumpus_world=wumpus_world,seed=seeds[world])
            # Armazena o melhor resultado e indivíduo da geração
            best_outputs.append(np.min(fitness))
            best_cromo.append(new_population[np.argmin(fitness)])
            best_current_state.append(current_state[np.argmin(fitness)])

            # Atualiza histórico do melhor fitness
            if generation == 0:
                best_fitness_all.append(np.min(fitness))
            elif np.min(fitness) < best_fitness_all[generation-1]:
                best_fitness_all.append(np.min(fitness))
            else:
                best_fitness_all.append(best_fitness_all[generation-1])

            # Seleção dos melhores (elitismo) e torneio
            elit_pop,size_elit = ga.elitism(new_population,fitness,elit_ratio)
            selected = [ga.selection(new_population,fitness,tournament_number) for i in range(size_pop-size_elit)]
            # Geração da próxima população com crossover e mutação
            offspring_crossover = ga.next_generation(selected,size_pop-size_elit,crossover_probability,mutation_probability,min,max)
            new_population = offspring_crossover + elit_pop

        # Após todas as gerações, avalia a última população
        fitness,current_state = ga.cal_pop_fitness(new_population,print_world=False,size_cromo=size_chromo,seed=seeds[worlds-1],wumpus_world=wumpus_world)
        best_outputs.append(np.min(fitness))
        best_cromo.append(new_population[np.argmin(fitness)])
        best_current_state.append(current_state[np.argmin(fitness)])

        # Atualiza histórico do melhor fitness final
        if np.min(fitness) < best_fitness_all[size_pop-1]:
            best_fitness_all.append(np.min(fitness))
        else:
            best_fitness_all.append(best_fitness_all[size_pop-1])

        # Coleta o índice do melhor indivíduo em todas as gerações
        idx = np.argmin(best_outputs) # iteração com a melhor solução

        print('Melhor Fitness em todas gerações: ')
        print(best_outputs[idx])

        print('Objetivos alcançados')
        print(best_current_state[idx])

        # Salva resultados do melhor indivíduo do teste
        results['fitness'].append(best_outputs[idx])
        results['test'].append(test)
        results['world'].append(world)
        results['gold'].append(best_current_state[idx][0])
        results['death_wumpus'].append(best_current_state[idx][1])
        results['win'].append(best_current_state[idx][2])
        results['alive'].append(best_current_state[idx][3])
        results['cromo'].append(best_cromo[idx])

# Salva os resultados em arquivo para análise posterior
filename = 'results/AG_dict_6x6_e6.pkl'
outfile = open(filename,'wb')
pickle.dump(results,outfile)
outfile.close()

# Exibe o tempo total de execução
print(time.time() - inicio)
winsound.Beep(800,2000)  # Sinal sonoro ao final

# O restante do código (comentado) pode ser usado para plotar gráficos dos resultados
# import matplotlib.pyplot
# matplotlib.pyplot.plot(best_outputs)
# matplotlib.pyplot.plot(best_fitness_all)
# matplotlib.pyplot.xlabel("Iteration")
# matplotlib.pyplot.ylabel("Fitness")
# matplotlib.pyplot.show()
