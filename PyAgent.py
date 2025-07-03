# PyAgent.py

import Action
import Orientation
import AgenteFirst
import AgenteGA
import AgenteLogico

agente = None  # Variável global para armazenar o agente atual

def PyAgent_Constructor(tipo = 1,aglist=None,max_movements=None,size_cromo=None):
    """ PyAgent_Constructor: chamado no início de uma nova rodada """
    
    global agente
    if tipo == 1:
        print("Agente em primeira pessoa")
        agente = AgenteFirst.AgentFirst()           # Cria agente controlado pelo usuário
    elif tipo == 2:
        print("Agente Lógico")
        agente = AgenteLogico.AgentLogico()         # Cria agente lógico (baseado em regras)
    else:
        #print("Agente AG")
        agente = AgenteGA.AgentGA(aglist,max_movements,size_cromo)  # Cria agente com Algoritmo Genético
    #print("PyAgent_Constructor")


def PyAgent_Destructor():
    """ PyAgent_Destructor: chamado após todas as tentativas de uma rodada """
    #print("PyAgent_Destructor")


def PyAgent_Initialize():
    """ PyAgent_Initialize: chamado no início de cada tentativa """
    #print("PyAgent_Initialize")


def PyAgent_Process(stench, breeze, glitter, bump, scream):
    """ PyAgent_Process: chamado com novas percepções após cada ação para retornar a próxima ação """
    return agente.process([stench, breeze, glitter, bump, scream])


def PyAgent_GameOver(score):
    """ PyAgent_GameOver: chamado ao final de cada tentativa """
    #print("PyAgent_GameOver: score = " + str(score))
