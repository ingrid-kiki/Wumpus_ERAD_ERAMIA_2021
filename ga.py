import numpy
from numpy import random
import WumpsimAG
import numpy as np
import time
def cal_pop_fitness(pop,print_world,size_cromo,wumpus_world,seed=50):
    # Calculating the fitness value of each solution in the current population.
    # The fitness function calulates the sum of products between each input and its corresponding weight.
	current_state = []
	fitness = []
	for i,cromo in enumerate(pop):
		avgscore, totalscore,has_gold,death_wumpus,win,alive = WumpsimAG.run(cromo,print_world=print_world,size_cromo=size_cromo,seed=seed,world_generated=wumpus_world)
		fitness.append(-1*totalscore)
		current_state.append([has_gold,death_wumpus,win,alive])
		random.seed(int(np.ceil(time.time())))
	return fitness,current_state

# tournament selection
def selection(pop, scores, k=3):
	# first random selection
	selection_ix = np.random.randint(len(pop))
	for ix in np.random.randint(0, len(pop), k-1):
		# check if better (e.g. perform a tournament)
		if scores[ix] < scores[selection_ix]:
			selection_ix = ix
	return pop[selection_ix]

def elitism(pop,scores,ratio):
	size = int(np.ceil(len(pop)*ratio))
	#print(size)
	pop = np.array(pop)
	elit_pop = pop[np.argsort(scores)]
	elit_pop = elit_pop[:size,:]
	return list(elit_pop),size


# crossover two parents to create two children
def crossover(p1, p2, r_cross):
	# children are copies of parents by default
	c1, c2 = p1.copy(), p2.copy()
	# check for recombination
	if np.random.rand() < r_cross:
		# select crossover point that is not on the end of the string
		pt = np.random.randint(1, len(p1)-2)
		# perform crossover
		c1 = list(p1[:pt]) + list(p2[pt:])
		c2 = list(p2[:pt]) + list(p1[pt:])
	return [c1, c2]

def next_generation(selected,n_pop,r_cross,r_mut,min,max):
    children = list()
    for i in range(0, n_pop, 2):
        # get selected parents in pairs
        p1, p2 = selected[i], selected[i+1]
        # crossover and mutation
        for c in crossover(p1, p2, r_cross):
            # mutation
            mutation(c, r_mut,min,max)
            # store for next generation
            children.append(c)
    return children

# mutation operator
def mutation(bitstring, r_mut,min,max):
	for i in range(len(bitstring)):
		# check for a mutation
		if np.random.rand() < r_mut:
			# flip the bit
			bitstring[i] = np.random.randint(low=min,high=max+1)


