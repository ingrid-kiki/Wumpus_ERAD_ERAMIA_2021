import WumpsimReative

import pickle

seed = 42
has_gold = 0
death_wumpus = 0
win = 0
tests = 1
worlds = 5
seeds = [43,44,45,46,50]
print_world = False #mostra a navegação do agente na tela.
results = {'totalscore':[],'test':[],'world':[],'gold':[],'death_wumpus':[],'win':[],"alive":[]}
def main(args):
    print(args.agente)
    if args.agente in [1,2]:
        for world in range(worlds):
            
            for test in range(tests):
                #seed = test*10
                avgscore, totalscore,has_gold,death_wumpus,win,alive = WumpsimReative.run(print_world=print_world,seed=seeds[world])
                results['totalscore'].append(totalscore)
                results['test'].append(test)
                results['world'].append(world)
                results['gold'].append(has_gold)
                results['death_wumpus'].append(death_wumpus)
                results['win'].append(win)
                results['alive'].append(alive)
    else:
        avgscore, totalscore = WumpsimReative.run(args)

    print("Objetivos (Pegou ouro,Matou Wumpus,Conseguiu Voltar) ",[has_gold,death_wumpus,win])

    print(results)

    filename = 'results/AG_reative_8x8.pkl'
    outfile = open(filename,'wb')
    pickle.dump(results,outfile)
    outfile.close()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-tries', type=int, default=1)
    parser.add_argument('-trials', type=int, default=1)
    parser.add_argument('-seed', type=int)
    parser.add_argument('-world', type=str)
    parser.add_argument('-agente', type=int)
    
    args = parser.parse_args()
    args.aglist = None
    if args.tries <= 0:
        raise argparse.ArgumentTypeError("Minimum tries is 1")

    if args.trials <= 0:
        raise argparse.ArgumentTypeError("Minimum trials is 1")

    if args.seed and args.seed <= 0:
        raise argparse.ArgumentTypeError("Seed must be a positive integer")

    main(args)