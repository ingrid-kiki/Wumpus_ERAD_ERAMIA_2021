import numpy as np
from numpy import random
from numpy.core.fromnumeric import size
import ga
import time
import pickle
from WumpsimAG import WumpusWorld
import winsound
#size_chromo = 200
#num_generations = 100
#size_pop = 100
#tournament_number = 4
size_world = 6
size_chromo = 200
size_pop = 100
#varbound = np.array([[0,6]]*size_chromo)
#sol_per_pop = 100
num_parents_mating = 2
num_generations = 100

crossover_probability = 0.5
mutation_probability = 0.15
tournament_number = 3
elit_ratio = 0.02
min = 0
max = 6

winsound.Beep(550,1000)




seed = 50
#tests = 20
#worlds = 5

tests = 10
worlds = 5

seeds = [43,44,45,46,50]

results = {'fitness':[],'test':[],'world':[],'gold':[],'death_wumpus':[],'win':[],'alive':[],'cromo':[]}
#fitness_all
#current_all
#cromo_all
#inicio = time.time()
inicio = time.time()
for world in range(worlds):
    #random.seed(world)
    #wumpus_world = WumpusWorld(file_information=None)
    #wumpus_world.initialize()
    wumpus_world = None
    for test in range(tests):
        best_outputs = []
        best_cromo = []
        best_fitness_all = []
        best_current_state = []
        random.seed(world + test + size_world)
        new_population = np.random.randint(low=min, high=max+1, size=(size_pop,size_chromo))
        for generation in range(num_generations):
            #print("Generation : ", generation)
            # Measuring the fitness of each chromosome in the population.
            fitness,current_state = ga.cal_pop_fitness(new_population,print_world=False,size_cromo=size_chromo,wumpus_world=wumpus_world,seed=seeds[world])
            
            #Armazena o melhor resultado e indivíduo e o que ele conseguiu no jogo
            best_outputs.append(np.min(fitness))
            best_cromo.append(new_population[np.argmin(fitness)])
            best_current_state.append(current_state[np.argmin(fitness)])

            if generation == 0:
                best_fitness_all.append(np.min(fitness))
            elif np.min(fitness) < best_fitness_all[generation-1]:
                best_fitness_all.append(np.min(fitness))
            else:
                best_fitness_all.append(best_fitness_all[generation-1])

            #print("Best result : ", np.min(fitness))

            #seleção por elitismo
            elit_pop,size_elit = ga.elitism(new_population,fitness,elit_ratio)
            selected = [ga.selection(new_population,fitness,tournament_number) for i in range(size_pop-size_elit)]
            #print(len(selected))
            # Gerando a próxima geração com crossover
            offspring_crossover = ga.next_generation(selected,size_pop-size_elit,crossover_probability,mutation_probability,min,max)
            new_population = offspring_crossover + elit_pop
            
        # Após a execução de todas as gerações, calcula o fitness e os melhores da última geração
        fitness,current_state = ga.cal_pop_fitness(new_population,print_world=False,size_cromo=size_chromo,seed=seeds[worlds-1],wumpus_world=wumpus_world)
        best_outputs.append(np.min(fitness))
        best_cromo.append(new_population[np.argmin(fitness)])
        best_current_state.append(current_state[np.argmin(fitness)])

        if np.min(fitness) < best_fitness_all[size_pop-1]:
                best_fitness_all.append(np.min(fitness))
        else:
            best_fitness_all.append(best_fitness_all[size_pop-1])
        
        #Define dicionário com os resultados de cada teste
        #Coleta o índice do melhor indivíduo em todas as gerações
        idx = np.argmin(best_outputs) #iteração com a melhor solução

        print('Melhor Fitness em todas gerações: ')
        print(best_outputs[idx])

        #print('Melhor Indivíduo: ')
        #print(best_cromo[idx])

        print('Objetivos alcançados')
        print(best_current_state[idx])

        #print('Geração com o melhor resultado: ')
        #print(idx)

        results['fitness'].append(best_outputs[idx])
        results['test'].append(test)
        results['world'].append(world)
        results['gold'].append(best_current_state[idx][0])
        results['death_wumpus'].append(best_current_state[idx][1])
        results['win'].append(best_current_state[idx][2])
        results['alive'].append(best_current_state[idx][3])
        results['cromo'].append(best_cromo[idx])

filename = 'results/AG_dict_6x6_e6.pkl'
outfile = open(filename,'wb')
pickle.dump(results,outfile)
outfile.close()

print(time.time() - inicio)
winsound.Beep(800,2000)
#print(results)
#elapsed = time.time() - inicio
#print(elapsed)
#import matplotlib.pyplot
#matplotlib.pyplot.plot(best_outputs)
#matplotlib.pyplot.plot(best_fitness_all)
#matplotlib.pyplot.xlabel("Iteration")
#matplotlib.pyplot.ylabel("Fitness")
#matplotlib.pyplot.show()
