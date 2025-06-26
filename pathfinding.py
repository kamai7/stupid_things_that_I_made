import random

class Node:
    def __init__(self,pos_x,pos_y):
        self.voisins = []
        self.pos_x = pos_x
        self.pos_y = pos_y

    def __str__(self):
        return "▮ " if len(self.voisins) == 0 else ". "
    
    def __getitem__(self,pos):
        return self.voisins[pos]
    
    def __eq__(self,other):
        if not isinstance(other,Node):
            return False
        return other.pos_x == self.pos_x and other.pos_y == self.pos_y and other.voisins == self.voisins

    

class Terrain:
    def __init__(self,taille_x,taille_y):
        self.taille_x = taille_x
        self.taille_y = taille_y
        self.a = []
        self.b = []

        self.grille = []
        for x in range(taille_x):
            self.grille.append([])
            for y in range(taille_y):
                self.grille[x].append(Node(x,y))

    def generate(self,amount):
        
        for x,line in enumerate(self.grille):
            for y,node in enumerate(line):
                for x_ in range(max(0,x-1),min(len(self.grille),x+2)):
                    for y_ in range(max(0,y-1),min(len(self.grille[x]),y+2)):
                        if (x_ == x or y_ == y) and not (x_ == x and y_ == y):
                            node.voisins.append(self[x_][y_])

        for line in self.grille:
            for node in line:
                if random.random()/(4 - 3/(len(node.voisins) + 1)) < amount:
                    for v in node.voisins:
                        v.voisins.remove(node)
                    node.voisins = []
                    

    def to_string(self,special_nodes=[],special_symbol="#"):
        ret = "     "
        for i in range(self.taille_x):
            ret +=f"{i%10} "

        ret += "\n    +" + "--" * self.taille_x + "+\n"

        for i,line in enumerate(self.grille):
            ret += f"{i})" + " " * (3-len(str(i))) + "|"
            for j,node in enumerate(line):

                if node in special_nodes:
                    if len(self.a) == 2 and i == self.a[0] and j == self.a[1]:
                        ret += "\033[92m" + special_symbol + "\033[00m "
                    elif len(self.b) == 2 and i == self.b[0] and j == self.b[1]:
                        ret += "\033[91m" + special_symbol + "\033[00m "
                    else:
                        ret += "\033[93m" + special_symbol + "\033[00m "
                else:
                    ret += str(node)
            ret += "|\n"
        
        ret += "    +" + "--" * self.taille_x + "+\n"

        return ret
    
    def define(self):
        try:
            a = input("define a(X,Y): ").split(",")
            self.a = []
            for coo in a:
                num = int(coo)
                if num >= self.taille_x or num < 0:
                    raise ValueError()
                self.a.append(num)
            if self[self.a[0]][self.a[1]].voisins == []:
                raise ValueError()
            b = input("define b(X,Y): ").split(",")
            self.b = []
            for coo in b:
                num = int(coo)
                if num >= self.taille_y or num < 0:
                    raise ValueError()
                self.b.append(int(coo))
            if self[self.b[0]][self.b[1]].voisins == [] or self.a == self.b:
                raise ValueError()
        except ValueError:
            print("retry:")
            self.define()

    def __getitem__(self,key):
        return self.grille[key]

class Solveur:
    def __init__(self,terrain):
        self.terrain = terrain
        if terrain.a == [] or terrain.b == []:
            terrain.define()
        self.a = terrain[terrain.a[0]][terrain.a[1]]
        self.b = terrain[terrain.b[0]][terrain.b[1]]

    def astar(self):
        checked = [self.a]
        neighbors = []
        for v in self.a:
            neighbors.insert(self.get_insertion_index(v,1,neighbors),(v,self.a,1))
        parcours = [(self.a,None,0)]
        solve = []

        while self.b not in checked:
            if len(neighbors) == 0:
                print('no solution')
                print(self.terrain.to_string(checked,"#"))
                break

            min = neighbors[0][0]
            parent = neighbors[0][1]
            distance = neighbors[0][2]

            checked.append(min)
            neighbors.pop(0)
            parcours.append((min,parent,distance))
            for v in min.voisins:
                if v not in checked:
                    neighbors.insert(self.get_insertion_index(v,distance + 1,neighbors),(v,min,distance + 1))
        else:
            print(self.terrain.to_string(checked))
            n = parcours[-1]
            while n[1] != None:
                solve.append(n[0])
                n = parcours[[parcour[0] for parcour in parcours].index(n[1])]
            solve.append(n[0])
            print(self.terrain.to_string(solve,"o"))

        print("\nnombre de chemins tentés: " + str(len(checked)) + "\nlongueur du chemin final: " + str(len(solve)))

    def get_insertion_index(self,node,distance,list):
        start = 0
        end = len(list)
        while start < end:
            mid = (start + end)//2
            val = list[mid][0]
            if abs(val.pos_x - self.b.pos_x) + abs(val.pos_y - self.b.pos_y) + list[mid][2] < abs(node.pos_x - self.b.pos_x)+ abs(node.pos_y - self.b.pos_y) + distance:
                start = mid + 1
            else:
                end = mid
        return start

random.seed(0)
terrain = Terrain(20,20)
terrain.generate(0.11)
print(terrain.to_string())
solveur = Solveur(terrain)
solveur.astar()
