# PyAgent.py

import Action
import Orientation
import AgenteFirst
import AgenteGA
import AgenteLogico

agente = None

def PyAgent_Constructor(tipo = 1,aglist=None,max_movements=None,size_cromo=None):
    """ PyAgent_Constructor: called at the start of a new trial """
    
    global agente
    if tipo == 1:
        print("Agente em primeira pessoa")
        agente = AgenteFirst.AgentFirst()
    elif tipo == 2:
        print("Agente Lógico")
        agente = AgenteLogico.AgentLogico()
    else:
        #print("Agente AG")
        agente = AgenteGA.AgentGA(aglist,max_movements,size_cromo)
    #print("PyAgent_Constructor")


def PyAgent_Destructor():
    """ PyAgent_Destructor: called after all tries for a trial are complete """
   #print("PyAgent_Destructor")


def PyAgent_Initialize():
    """ PyAgent_Initialize: called at the start of a new try """
    #print("PyAgent_Initialize")


def PyAgent_Process(stench, breeze, glitter, bump, scream):
    """ PyAgent_Process: called with new percepts after each action to return the next action """

    return agente.process([stench, breeze, glitter, bump, scream])


def PyAgent_GameOver(score):
    """ PyAgent_GameOver: called at the end of each try """
    #print("PyAgent_GameOver: score = " + str(score))