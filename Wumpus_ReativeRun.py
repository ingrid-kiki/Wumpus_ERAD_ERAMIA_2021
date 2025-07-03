import WumpsimReative
import pickle

# Parâmetros iniciais e variáveis de controle
seed = 42
has_gold = 0
death_wumpus = 0
win = 0
tests = 1                # Quantidade de testes por mundo
worlds = 5               # Quantidade de mundos diferentes
seeds = [43,44,45,46,50] # Sementes para geração dos mundos
print_world = False      # Se True, mostra a navegação do agente na tela

# Dicionário para armazenar resultados dos testes
results = {
    'totalscore': [],
    'test': [],
    'world': [],
    'gold': [],
    'death_wumpus': [],
    'win': [],
    "alive": []
}

def main(args):
    # Exibe o tipo de agente selecionado
    print(args.agente)
    # Executa para agentes do tipo 1 (manual) ou 2 (lógico)
    if args.agente in [1,2]:
        for world in range(worlds):
            for test in range(tests):
                # Executa o simulador para o mundo e teste atual
                avgscore, totalscore, has_gold, death_wumpus, win, alive = WumpsimReative.run(
                    print_world=print_world, seed=seeds[world]
                )
                # Armazena os resultados do teste
                results['totalscore'].append(totalscore)
                results['test'].append(test)
                results['world'].append(world)
                results['gold'].append(has_gold)
                results['death_wumpus'].append(death_wumpus)
                results['win'].append(win)
                results['alive'].append(alive)
    else:
        # Para outros tipos de agente, executa passando os argumentos diretamente
        avgscore, totalscore = WumpsimReative.run(args)

    # Exibe os objetivos alcançados pelo agente
    print("Objetivos (Pegou ouro, Matou Wumpus, Conseguiu Voltar) ", [has_gold, death_wumpus, win])

    # Exibe o dicionário de resultados
    print(results)

    # Salva os resultados em arquivo para análise posterior
    filename = 'results/AG_reative_8x8.pkl'
    outfile = open(filename, 'wb')
    pickle.dump(results, outfile)
    outfile.close()

if __name__ == '__main__':
    import argparse

    # Configuração dos argumentos de linha de comando
    parser = argparse.ArgumentParser()
    parser.add_argument('-tries', type=int, default=1)
    parser.add_argument('-trials', type=int, default=1)
    parser.add_argument('-seed', type=int)
    parser.add_argument('-world', type=str)
    parser.add_argument('-agente', type=int)
    
    args = parser.parse_args()  # Faz o parsing dos argumentos da linha de comando
    args.aglist = None         # Inicializa a lista de ações do agente como None (padrão)

    # Validação dos argumentos recebidos pela linha de comando
    if args.tries <= 0:
        # Garante que o número de tentativas seja pelo menos 1
        raise argparse.ArgumentTypeError("Minimum tries is 1")

    if args.trials <= 0:
        # Garante que o número de execuções (trials) seja pelo menos 1
        raise argparse.ArgumentTypeError("Minimum trials is 1")

    if args.seed and args.seed <= 0:
        # Garante que a semente, se fornecida, seja positiva
        raise argparse.ArgumentTypeError("Seed must be a positive integer")

    # Chama a função principal do programa, passando os argumentos validados
    main(args)
