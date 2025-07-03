import Action

##########################################################################################
# Classe que representa um nó (célula) do mundo Wumpus
class Wumpus_Node:

    def __init__(self,row,col):
        self.row = row
        self.column = col
        self.name = str(row) + "," + str(col)  # Nome do nó (ex: "1,1")
        self.right = ""  # Estado à direita
        self.left = ""   # Estado à esquerda
        self.up = ""     # Estado acima
        self.down = ""   # Estado abaixo

    def __repr__(self):
        # Representação textual do nó
        return ("(Name : " + str(self.name) + " , " +
                " left : " + self.left + " , " + " Right : " + self.right + " , " +
                " Up : " + self.up + " , " + " Down : " + self.down + " , " + ")")

##########################################################################################        
# Classe que representa o jogador/agente no mundo Wumpus
class Wumpus_Player:

    def __init__(self , state , direction):
        self.current_state = state           # Estado atual (posição)
        self.current_direction = direction   # Direção atual
        self.has_gold = False               # Se já pegou o ouro
        self.has_killed_wumpus = False      # Se já matou o Wumpus
        self.is_leaving = False             # Se está saindo do mundo

    def move(self,states):
        # Move o agente para o próximo estado, se possível
        if self.current_direction=="Right" and states[self.current_state].right!="W":
            self.current_state=states[self.current_state].right
        elif self.current_direction=="Left" and states[self.current_state].left!="W":
            self.current_state=states[self.current_state].left
        elif self.current_direction=="Up" and states[self.current_state].up!="W":
            self.current_state=states[self.current_state].up
        elif self.current_direction=="Down" and states[self.current_state].down!="W":
            self.current_state=states[self.current_state].down

    def turn_left(self):
        # Gira o agente para a esquerda
        if self.current_direction=="Right":
            self.current_direction="Up"
        elif self.current_direction=="Left":
            self.current_direction="Down"
        elif self.current_direction=="Up":
            self.current_direction="Left"
        elif self.current_direction=="Down":
            self.current_direction="Right"

    def turn_right(self):
        # Gira o agente para a direita
        if self.current_direction=="Right":
            self.current_direction="Down"
        elif self.current_direction=="Left":
            self.current_direction="Up"
        elif self.current_direction=="Up":
            self.current_direction="Right"
        elif self.current_direction=="Down":
            self.current_direction="Left"

    def __repr__(self):
        # Representação textual do agente
        return ("Current State : " + str(self.current_state.name) + " , " +
                "Current Direction : " + str(self.current_direction))

############################################################################# 
# Classe que representa todos os estados do mundo Wumpus
class Wumpus_States:

    def __init__(self):
        self.states = dict()                # Dicionário de estados
        self.visited_states = []            # Lista de estados visitados
        self.unvisited_safe_states = []     # Lista de estados seguros não visitados
        self.max_row = 8                    # Número máximo de linhas
        self.max_col = 8                    # Número máximo de colunas

    def add_state(self,node):
        # Adiciona um novo estado ao mundo e define suas conexões
        if self.max_col!=-1 and node.column==self.max_col:
            node.right="W"
        else:
            node.right=str(node.row)+","+str(node.column+1)
        
        if node.column-1==0:
            node.left="W"
        else:
            node.left=str(node.row)+","+str(node.column-1)
        
        if self.max_row!=-1 and node.row==self.max_row:
            node.up="W"
        else:
            node.up=str(node.row+1)+","+str(node.column)
        
        if node.row-1==0:
            node.down="W"
        else:
            node.down=str(node.row-1)+","+str(node.column)
        
        self.states[node.name]=node
        if node.name not in self.visited_states:
            self.visited_states.append(node.name)

    def __repr__(self):
        # Representação textual dos estados
        return ("States : " + str(self.states.keys()) + " , " +
                " Visited States : " + str(self.visited_states))

#########################################################################################
# Base de conhecimento para lógica do agente
class Knowledge_Base:
    
    def __init__(self):
        self.KB=[]
        
    def add(self,sentence):
        # Adiciona uma sentença à base de conhecimento
        if sentence not in self.KB:
            self.KB.append(sentence)
            self.KB=sorted(self.KB,key=lambda x:len(x))
        
    def check(self,query):
        # Verifica se uma query está na base de conhecimento
        KB_temp=[[item2 for item2 in item] for item in self.KB]
        KB_temp.append(query)
        KB_temp=sorted(KB_temp,key=lambda x:len(x))
        for item1 in KB_temp:
            if len(item1)>0:
                for item2 in KB_temp:
                    self.compare(item1,item2)
            else:
                return True
        return False           
                
    def compare(self,Query1,Query2):
        # Compara duas queries para resolução lógica
        if len(Query1)==1:    
            for item in Query2:
                if Query1[0][0]=="~" and item[0:]==Query1[0][1:]:
                    Query2.remove(item)
                elif item[0]=="~" and Query1[0][0:]==item[1:]:
                    Query2.remove(item)
                    
    def remove(self,sentence):
        # Remove uma sentença da base de conhecimento
        for item1 in self.KB:
            for item2 in item1:
                if item2==sentence or item2==("~"+sentence):
                    item1.remove(item2)
            if len(item1)==0:
                self.KB.remove(item1)        

############################################################################################
from queue import PriorityQueue

# Classe para busca de custo uniforme (unicost)
class Cost_Search:
    def __init__(self,graph,start,goals,visited_states,current_direction):
        self.start=start
        self.goals=goals
        self.visited_states=visited_states
        self.current_direction=current_direction
        self.graph=graph
        
    def unicost(self):
        # Busca caminho de menor custo até um dos objetivos
        q = PriorityQueue()
        expansion = [[0,self.current_direction,self.start,[self.start]]]
        if self.start in self.goals:
            return [expansion[-1][0],expansion[-1][3]]  
        for item in ["Right","Up","Left","Down"]:
            if item=="Right":
                if self.graph[self.start].right in self.visited_states or self.graph[self.start].right in self.goals:
                    cost=self.movement_cost(self.current_direction, "Right")
                    q.put([cost,"Right",self.graph[self.start].right,[self.start]+[self.graph[self.start].right]])
            elif item=="Up":
                if self.graph[self.start].up in self.visited_states or self.graph[self.start].up in self.goals:
                    cost=self.movement_cost(self.current_direction, "Up")
                    q.put([cost,"Up",self.graph[self.start].up,[self.start]+[self.graph[self.start].up]])
            elif item=="Left": 
                if self.graph[self.start].left in self.visited_states or self.graph[self.start].left in self.goals:
                    cost=self.movement_cost(self.current_direction, "Left")
                    q.put([cost,"Left",self.graph[self.start].left,[self.start]+[self.graph[self.start].left]])
            elif item=="Down":
                if self.graph[self.start].down in self.visited_states or self.graph[self.start].down in self.goals:
                    cost=self.movement_cost(self.current_direction, "Down")
                    q.put([cost,"Down",self.graph[self.start].down,[self.start]+[self.graph[self.start].down]])
        
        while True:
            current=q.get()
            expansion.append(current)
            if current[2] in self.goals:
                break
            else:
                for item in ["Right","Up","Left","Down"]:
                    if item=="Right":
                        if self.graph[current[2]].right in self.visited_states or self.graph[current[2]].right in self.goals:
                            path=current[3]+[self.graph[current[2]].right]
                            cost=self.movement_cost(current[1], "Right")+current[0]
                            q.put([cost,"Right",self.graph[current[2]].right,path])
                    elif item=="Up":
                        if self.graph[current[2]].up in self.visited_states or self.graph[current[2]].up in self.goals:
                            path=current[3]+[self.graph[current[2]].up]
                            cost=self.movement_cost(current[1], "Up")+current[0]
                            q.put([cost,"Up",self.graph[current[2]].up,path])
                    elif item=="Left":
                        if self.graph[current[2]].left in self.visited_states or self.graph[current[2]].left in self.goals:
                            path=current[3]+[self.graph[current[2]].left]
                            cost=self.movement_cost(current[1], "Left")+current[0]
                            q.put([cost,"Left",self.graph[current[2]].left,path])
                    elif item=="Down":
                        if self.graph[current[2]].down in self.visited_states or self.graph[current[2]].down in self.goals:
                            path=current[3]+[self.graph[current[2]].down]
                            cost=self.movement_cost(current[1], "Down")+current[0]
                            q.put([cost,"Down",self.graph[current[2]].down,path])
                               
        return [expansion[-1][0],expansion[-1][3][1:]]  
            
    def movement_cost(self,current,next):
        # Calcula o custo de movimentação entre direções
        if current==next:
            return 1
        elif current=="Right":
            if next=="Left":
                return 3
            else:
                return 2
        elif current=="Up":
            if next=="Down":
                return 3
            else:
                return 2
        elif current=="Left":
            if next=="Right":
                return 3
            else:
                return 2
        elif current=="Down":
            if next=="Up":
                return 3
            else:
                return 2

##################################################################################################################################
# Classe principal do agente lógico (MyAI)
class MyAI ():
    def __init__ ( self ):
        self.states = Wumpus_States()           # Estados do mundo
        self.states.add_state(Wumpus_Node(1,1)) # Estado inicial
        self.player = Wumpus_Player("1,1","Right") # Agente começa em (1,1) virado para a direita
        self.KB=Knowledge_Base()                # Base de conhecimento
        self.KB.add(["~P1,1"])                 # Não há poço na origem
        self.KB.add(["~W1,1"])                 # Não há Wumpus na origem
        self.wumpus_dead=False                 # Estado do Wumpus
        self.wumpus_directions = ["Right","Left","Up","Down"]
        self.arrow_shot = False                # Se já atirou a flecha
        self.exit = False                      # Se está saindo do mundo
        self.moves = []                        # Lista de movimentos planejados
        self.killing_wumpus = False            # Se está tentando matar o Wumpus
        self.start_stench = False              # Se começou a sentir fedor

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # Função principal que decide a ação do agente baseado nas percepções

        if bump:
            self.handle_bump()

        current_node=self.states.states[self.player.current_state]
        
        # Estratégia para atirar a flecha se sentir fedor na origem
        if current_node.name == "1,1" and stench and not breeze and not self.arrow_shot and not self.exit:
            self.arrow_shot=True
            self.start_stench = True
            return Action.SHOOT
            
        # Se ouviu o grito do Wumpus morrendo
        if scream:
            self.start_stench=False
            self.clear_base()
            self.killing_wumpus=False
            self.wumpus_dead=True
            for item in self.KB.KB:
                if item[0][0]=="S":
                    name = item[0][1:]
                    breeze_check = "~B"+item[0][1:]
                    node = self.states.states[name]
                    if not self.KB.check([breeze_check]):
                        if node.right not in self.states.visited_states and node.right not in self.states.unvisited_safe_states and node.right !="W":
                            self.states.unvisited_safe_states.append(node.right)
                        if node.up not in self.states.visited_states and node.up not in self.states.unvisited_safe_states and node.up !="W":
                            self.states.unvisited_safe_states.append(node.up)
                        if node.left not in self.states.visited_states and node.left not in self.states.unvisited_safe_states and node.left !="W":
                            self.states.unvisited_safe_states.append(node.left)
                        if node.down not in self.states.visited_states and node.down not in self.states.unvisited_safe_states and node.down !="W":
                            self.states.unvisited_safe_states.append(node.down)
        elif self.start_stench:
            self.start_stench=False
            self.KB.add(["W2,1"])
            self.KB.add(["~W1,2"])

        # Atualiza base de conhecimento e estados conforme percepções
        if not self.exit and not self.killing_wumpus:
            if not self.wumpus_dead:
                if stench:
                    self.handle_stench(current_node)
                    self.wumpus_check(current_node)      
                else:
                    self.handle_no_stench(current_node)
            if breeze:
                self.handle_breeze(current_node)
            else:
                self.handle_no_breeze(current_node) 
            
            self.safe_check(current_node)
            
            # Planeja movimentos: pegar ouro, explorar ou sair
            if not self.killing_wumpus:
                if glitter:
                    self.exit = True
                    search=Cost_Search(self.states.states,self.player.current_state,["1,1"],self.states.visited_states,self.player.current_direction)
                    cost_path = search.unicost()
                    self.moves = self.move_list(cost_path[1])
                    self.moves.insert(0,"g")
                elif len(self.states.unvisited_safe_states)>0:
                    search=Cost_Search(self.states.states,self.player.current_state,self.states.unvisited_safe_states,self.states.visited_states,self.player.current_direction)
                    cost_path = search.unicost()
                    self.moves = self.move_list(cost_path[1])
                else:
                    self.exit = True
                    search=Cost_Search(self.states.states,self.player.current_state,["1,1"],self.states.visited_states,self.player.current_direction)
                    cost_path = search.unicost()
                    self.moves = self.move_list(cost_path[1])

        # Executa o próximo movimento planejado
        move=self.moves.pop(0)
        if move=="l":
            self.player.turn_left()
            return Action.TURNLEFT
        elif move=="r":
            self.player.turn_right()
            return Action.TURNRIGHT
        elif move=="w":
            self.walk()
            return Action.GOFORWARD
        elif move=="s":
            return Action.SHOOT
        elif move=="c":
            return Action.CLIMB
        elif move=="g":
            return Action.GRAB

    # Limpa sentenças relacionadas ao Wumpus da base de conhecimento
    def clear_base(self):
        to_remove=[]
        for item in self.KB.KB:
            if item[0][0]=="W" or item[0][1]=="W":
                to_remove.append(item)
        for item in to_remove:
            self.KB.KB.remove(item)

    # Verifica e planeja matar o Wumpus se possível
    def wumpus_check(self,current_node):
        row = current_node.row
        col = current_node.column
        if not self.arrow_shot:
            if current_node.right!="W":
                if self.KB.check(["W"+str(row-1)+","+str(col)]) and self.KB.check(["~S"+str(row-1)+","+str(col+1)]) or self.KB.check(["W"+str(row+1)+","+str(col)]) and self.KB.check(["~S"+str(row+1)+","+str(col+1)]):
                    self.kill_wumpus("Right")
            if current_node.up!="W":
                if self.KB.check(["W"+str(row)+","+str(col-1)]) and self.KB.check(["~S"+str(row+1)+","+str(col-1)]) or self.KB.check(["W"+str(row)+","+str(col+1)]) and self.KB.check(["~S"+str(row+1)+","+str(col+1)]):
                    self.kill_wumpus("Up")
            if current_node.left!="W":
                if self.KB.check(["W"+str(row-1)+","+str(col)]) and self.KB.check(["~S"+str(row-1)+","+str(col-1)]) or self.KB.check(["W"+str(row+1)+","+str(col)]) and self.KB.check(["~S"+str(row+1)+","+str(col-1)]):
                    self.kill_wumpus("Left")
            if current_node.down!="W":
                if self.KB.check(["W"+str(row)+","+str(col-1)]) and self.KB.check(["~S"+str(row-1)+","+str(col-1)]) or self.KB.check(["W"+str(row)+","+str(col+1)]) and self.KB.check(["~S"+str(row-1)+","+str(col+1)]):
                    self.kill_wumpus("Down")

    # Planeja movimentos para matar o Wumpus em determinada direção
    def kill_wumpus(self,direction):
        self.killing_wumpus=True
        self.moves=[]
        if direction == "Right":
            if self.player.current_direction=="Right":
                self.moves.insert(0,"s")
            elif self.player.current_direction=="Up":
                self.moves.insert(0,"s")
                self.moves.insert(0,"r")
            elif self.player.current_direction=="Left":
                self.moves.insert(0,"s")
                self.moves.insert(0,"r")
                self.moves.insert(0,"r")
            elif self.player.current_direction=="Down":
                self.moves.insert(0,"s")
                self.moves.insert(0,"l")
        elif direction == "Up":
            if self.player.current_direction=="Right":
                self.moves.insert(0,"s")
                self.moves.insert(0,"l")
            elif self.player.current_direction=="Up":
                self.moves.insert(0,"s")
            elif self.player.current_direction=="Left":
                self.moves.insert(0,"s")
                self.moves.insert(0,"r")
            elif self.player.current_direction=="Down":
                self.moves.insert(0,"s")
                self.moves.insert(0,"r")
                self.moves.insert(0,"r")
        elif direction == "Left":
            if self.player.current_direction=="Right":
                self.moves.insert(0,"s")
                self.moves.insert(0,"r")
                self.moves.insert(0,"r")
            elif self.player.current_direction=="Up":
                self.moves.insert(0,"s")
                self.moves.insert(0,"l")
            elif self.player.current_direction=="Left":
                self.moves.insert(0,"s")
            elif self.player.current_direction=="Down":
                self.moves.insert(0,"s")
                self.moves.insert(0,"r")
        elif direction == "Down":
            if self.player.current_direction=="Right":
                self.moves.insert(0,"s")
                self.moves.insert(0,"r")
            elif self.player.current_direction=="Up":
                self.moves.insert(0,"s")
                self.moves.insert(0,"r")
                self.moves.insert(0,"r")
            elif self.player.current_direction=="Left":
                self.moves.insert(0,"s")
                self.moves.insert(0,"l")
            elif self.player.current_direction=="Down":
                self.moves.insert(0,"s")

    # Atualiza lista de estados seguros não visitados
    def safe_check(self,current_node):
        if not self.wumpus_dead:
            if current_node.right!="W" and current_node.right not in self.states.visited_states and current_node.right not in self.states.unvisited_safe_states:
                if self.KB.check(["P"+current_node.right]) and self.KB.check(["W"+current_node.right]):
                    self.states.unvisited_safe_states.append(current_node.right)
            if current_node.up!="W" and current_node.up not in self.states.visited_states and current_node.up not in self.states.unvisited_safe_states:
                if self.KB.check(["P"+current_node.up]) and self.KB.check(["W"+current_node.up]):
                    self.states.unvisited_safe_states.append(current_node.up)
            if current_node.left!="W" and current_node.left not in self.states.visited_states and current_node.left not in self.states.unvisited_safe_states:
                if self.KB.check(["P"+current_node.left]) and self.KB.check(["W"+current_node.left]):
                    self.states.unvisited_safe_states.append(current_node.left)
            if current_node.down!="W" and current_node.down not in self.states.visited_states and current_node.down not in self.states.unvisited_safe_states:
                if self.KB.check(["P"+current_node.down]) and self.KB.check(["W"+current_node.down]):
                    self.states.unvisited_safe_states.append(current_node.down)
        else:
            if current_node.right!="W" and current_node.right not in self.states.visited_states and current_node.right not in self.states.unvisited_safe_states:
                if self.KB.check(["P"+current_node.right]):
                    self.states.unvisited_safe_states.append(current_node.right)
            if current_node.up!="W" and current_node.up not in self.states.visited_states and current_node.up not in self.states.unvisited_safe_states:
                if self.KB.check(["P"+current_node.up]):
                    self.states.unvisited_safe_states.append(current_node.up)
            if current_node.left!="W" and current_node.left not in self.states.visited_states and current_node.left not in self.states.unvisited_safe_states:
                if self.KB.check(["P"+current_node.left]):
                    self.states.unvisited_safe_states.append(current_node.left)
            if current_node.down!="W" and current_node.down not in self.states.visited_states and current_node.down not in self.states.unvisited_safe_states:
                if self.KB.check(["P"+current_node.down]):
                    self.states.unvisited_safe_states.append(current_node.down)    

    # Atualiza limites do mundo ao bater em uma parede
    def handle_bump(self):
        if self.player.current_direction=="Right":
            self.states.states.pop(self.player.current_state)
            self.states.visited_states.remove(self.player.current_state)
            state=self.player.current_state.split(",")
            self.player.current_state=state[0]+","+str(int(state[1])-1)
            self.states.max_col=int(state[1])-1
            row_col=self.player.current_state.split(",")
            new_state=Wumpus_Node(int(row_col[0]),int(row_col[1]))
            self.states.add_state(new_state)
            to_remove=[]
            for item in self.states.unvisited_safe_states:
                row_col=item.split(",")
                if int(row_col[1])==self.states.max_col+1:
                    to_remove.append(item)
            for item in to_remove:
                self.states.unvisited_safe_states.remove(item)
                
        elif self.player.current_direction=="Up":
            self.states.states.pop(self.player.current_state)
            self.states.visited_states.remove(self.player.current_state)
            state=self.player.current_state.split(",")
            self.player.current_state=str(int(state[0])-1)+","+state[1]
            self.states.max_row=int(state[0])-1
            row_col=self.player.current_state.split(",")
            new_state=Wumpus_Node(int(row_col[0]),int(row_col[1]))
            self.states.add_state(new_state)
            to_remove=[]
            for item in self.states.unvisited_safe_states:
                row_col=item.split(",")
                if int(row_col[0])==self.states.max_row+1:
                    to_remove.append(item)
            for item in to_remove:
                self.states.unvisited_safe_states.remove(item)

    # Atualiza base de conhecimento ao sentir fedor
    def handle_stench(self,current_node):
        sentence = []
        if current_node.right not in self.states.visited_states and current_node.right!="W":
            sentence.append("W"+current_node.right) 
        if current_node.up not in self.states.visited_states and current_node.up!="W":
            sentence.append("W"+current_node.up) 
        if current_node.left not in self.states.visited_states and current_node.left!="W":
            sentence.append("W"+current_node.left) 
        if current_node.down not in self.states.visited_states and current_node.down!="W":
            sentence.append("W"+current_node.down) 
        self.KB.add(sentence)
        self.KB.add(["S"+current_node.name])
        
    # Atualiza base de conhecimento ao sentir brisa
    def handle_breeze(self,current_node):
        sentence = []
        if current_node.right not in self.states.visited_states and current_node.right!="W":
            sentence.append("P"+current_node.right) 
        if current_node.up not in self.states.visited_states and current_node.up!="W":
            sentence.append("P"+current_node.up) 
        if current_node.left not in self.states.visited_states and current_node.left!="W":
            sentence.append("P"+current_node.left) 
        if current_node.down not in self.states.visited_states and current_node.down!="W":
            sentence.append("P"+current_node.down) 
        self.KB.add(sentence)
        self.KB.add(["B"+current_node.name])
    
    # Atualiza base de conhecimento ao NÃO sentir brisa
    def handle_no_breeze(self,current_node):
        if current_node.right not in self.states.visited_states and current_node.right!="W":
            self.KB.add(["~P"+current_node.right]) 
        if current_node.up not in self.states.visited_states and current_node.up!="W":
            self.KB.add(["~P"+current_node.up]) 
        if current_node.left not in self.states.visited_states and current_node.left!="W":
            self.KB.add(["~P"+current_node.left]) 
        if current_node.down not in self.states.visited_states and current_node.down!="W":
            self.KB.add(["~P"+current_node.down]) 
            
    # Atualiza base de conhecimento ao NÃO sentir fedor
    def handle_no_stench(self,current_node):
        if current_node.right not in self.states.visited_states and current_node.right!="W":
            self.KB.add(["~W"+current_node.right]) 
        if current_node.up not in self.states.visited_states and current_node.up!="W":
            self.KB.add(["~W"+current_node.up]) 
        if current_node.left not in self.states.visited_states and current_node.left!="W":
            self.KB.add(["~W"+current_node.left]) 
        if current_node.down not in self.states.visited_states and current_node.down!="W":
            self.KB.add(["~W"+current_node.down]) 
            
    # Move o agente para o próximo estado
    def walk(self):
        self.player.move(self.states.states)
        row_col=self.player.current_state.split(",")
        state=Wumpus_Node(int(row_col[0]),int(row_col[1]))
        self.states.add_state(state)
        if state.name in self.states.unvisited_safe_states:
            self.states.unvisited_safe_states.remove(state.name)
            
    # Gera lista de movimentos para seguir um caminho
    def move_list(self,path):
        direction = self.player.current_direction
        state = self.player.current_state
        current_node = self.states.states[state]
        move_list =[]
        for item in path:
            if direction=="Right":
                if item == current_node.right:
                    move_list.append('w')
                    try:
                        current_node = self.states.states[current_node.right]
                    except:
                        pass
                elif item == current_node.up:
                    move_list.append('l')
                    move_list.append('w')
                    direction = "Up"
                    try:
                        current_node = self.states.states[current_node.up]
                    except:
                        pass
                elif item == current_node.down:
                    move_list.append('r')
                    move_list.append('w')
                    direction = "Down"
                    try:
                        current_node = self.states.states[current_node.down]
                    except:
                        pass
                elif item == current_node.left:
                    move_list.append('r')
                    move_list.append('r')
                    move_list.append('w')
                    direction = "Left"
                    try:
                        current_node = self.states.states[current_node.left]
                    except:
                        pass
            elif direction=="Up":
                if item == current_node.right:
                    move_list.append('r')
                    move_list.append('w')
                    direction = "Right"
                    try:
                        current_node = self.states.states[current_node.right]
                    except:
                        pass
                elif item == current_node.up:
                    move_list.append('w')
                    try:
                        current_node = self.states.states[current_node.up]
                    except:
                        pass
                elif item == current_node.down:
                    move_list.append('r')
                    move_list.append('r')
                    move_list.append('w')
                    direction = "Down"
                    try:
                        current_node = self.states.states[current_node.down]
                    except:
                        pass
                elif item == current_node.left:
                    move_list.append('l')
                    move_list.append('w')
                    direction = "Left"
                    try:
                        current_node = self.states.states[current_node.left]
                    except:
                        pass
            elif direction=="Left":
                if item == current_node.right:
                    move_list.append('r')
                    move_list.append('r')
                    move_list.append('w')
                    direction = "Right"
                    try:
                        current_node = self.states.states[current_node.right]
                    except:
                        pass
                elif item == current_node.up:
                    move_list.append('r')
                    move_list.append('w')
                    direction = "Up"
                    try:
                        current_node = self.states.states[current_node.up]
                    except:
                        pass
                elif item == current_node.down:
                    move_list.append('l')
                    move_list.append('w')
                    direction = "Down"
                    try:
                        current_node = self.states.states[current_node.down]
                    except:
                        pass
                elif item == current_node.left:
                    move_list.append('w')
                    try:
                        current_node = self.states.states[current_node.left]
                    except:
                        pass
            elif direction=="Down":
                if item == current_node.right:
                    move_list.append('l')
                    move_list.append('w')
                    direction = "Right"
                    try:
                        current_node = self.states.states[current_node.right]
                    except:
                        pass
                elif item == current_node.up:
                    move_list.append('r')
                    move_list.append('r')
                    move_list.append('w')
                    direction = "Up"
                    try:
                        current_node = self.states.states[current_node.up]
                    except:
                        pass
                elif item == current_node.down:
                    move_list.append('w')
                    try:
                        current_node = self.states.states[current_node.down]
                    except:
                        pass
                elif item == current_node.left:
                    move_list.append('r')
                    move_list.append('w')
                    direction = "Left"
                    try:
                        current_node = self.states.states[current_node.left]
                    except:
                        pass
        if self.exit:
            move_list.append("c")
        return move_list

