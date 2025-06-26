import time

class Case:
    def __init__(self,alive=False):
        self.alive = alive
        self.neighbours = []

    def update(self):
        alive_neighbours = 0
        for neighbour in self.neighbours:
                if neighbour.alive:
                    alive_neighbours += 1

        if self.alive:
            if alive_neighbours < 2 or alive_neighbours > 3:
                self.alive = False
        elif alive_neighbours == 3:
            self.alive = True

class Jeu:
    def __init__(self,taille_x,taille_y,default=[]):
        self.counter =  0
        self.taille_x = taille_x
        self.taille_y = taille_y
        self.world = []
        for x in range(taille_x):
            self.world.append([])
            for y in range(taille_y):
                if [x,y] in default:
                    self.world[x].append(Case(alive=True))
                else:
                    self.world[x].append(Case(alive=False))

    def next(self):
        self.counter += 1
        copy = []
        for x in range(self.taille_x):
            copy.append([])
            for y in range(self.taille_y):
                copy[x].append(Case(self.world[x][y].alive))

        for i,line in enumerate(self.world):
            for j,case in enumerate(line):
                neighbours = []
                for x in range(max(0,i-1),min(len(self.world),i+2)):
                    for y in range(max(0,j-1),min(len(self.world[i]),j+2)):
                        if x != i or y != j:
                            neighbours.append(copy[x][y])
                case.neighbours = neighbours

        for line in self.world:
            for case in line:
                case.update()

    def print(self):
        print("+",end="")
        for i in range(self.taille_y):
            print("--",end="")
        print("+")

        for line in self.world:
            print("|",end="")
            for case in line:
                if case.alive:
                    print("■ ",end="")
                else:
                    print(". ",end="")
            print("|")
        
        print("+",end="")
        for i in range(self.taille_y):
            print("--",end="")
        print("+\n" + str(self.counter))
        for i in range(self.taille_y+3):
            print("\x1b[1A",end="")
    
class Bestiary:
    def glider(y, x):
        return [[y, x-2], [y, x-1], [y, x], [y-1, x], [y-2, x-1]]

    def blinker(y, x):
        return [[y, x], [y+1, x], [y-1, x]]
    
    def cube(y, x):
        return [[y+1, x+1], [y+1, x], [y, x+1], [y, x]]

    def factory(y, x):
        ret = Bestiary.cube(y+4, x) + Bestiary.cube(y+2, x+34) + Bestiary.blinker(y+5, x+10) + Bestiary.blinker(y+5, x+16) + Bestiary.blinker(y+3, x+20) + Bestiary.blinker(y+3, x+21)
        ret += [[y+3, x+11], [y+7, x+11], [y+2, x+12], [y+8, x+12], [y+2, x+13], [y+8, x+13], [y+5, x+14], [y+3, x+15], [y+7, x+15], [y+5, x+17], [y+1, x+22], [y+5, x+22], [y, x+24], [y+1, x+24], [y+5, x+24], [y+6, x+24]]
        return ret

    def toad(y, x):
        return [[y, x+1], [y, x+2], [y, x+3], [y+1, x], [y+1, x+1], [y+1, x+2]]

    def beacon(y, x):
        return [[y, x], [y, x+1], [y+1, x], [y+2, x+3], [y+3, x+2], [y+3, x+3]]

    def pulsar(y, x):
        coords = []
        offsets = [
            (0, 2), (0, 3), (0, 4), (0, 8), (0, 9), (0, 10),
            (5, 2), (5, 3), (5, 4), (5, 8), (5, 9), (5, 10),
            (7, 2), (7, 3), (7, 4), (7, 8), (7, 9), (7, 10),
            (12, 2), (12, 3), (12, 4), (12, 8), (12, 9), (12, 10),
            (2, 0), (3, 0), (4, 0), (8, 0), (9, 0), (10, 0),
            (2, 5), (3, 5), (4, 5), (8, 5), (9, 5), (10, 5),
            (2, 7), (3, 7), (4, 7), (8, 7), (9, 7), (10, 7),
            (2, 12), (3, 12), (4, 12), (8, 12), (9, 12), (10, 12)
        ]
        for dy, dx in offsets:
            coords.append([y + dy, x + dx])
        return coords

    def lwss(y, x):
        return [[y, x+1], [y, x+4], [y+1, x], [y+2, x], [y+2, x+4], [y+3, x], [y+3, x+1], [y+3, x+2], [y+3, x+3]]

    def tub(y, x):
        return [[y, x+1], [y+1, x], [y+1, x+2], [y+2, x+1]]

    def boat(y, x):
        return [[y, x], [y, x+1], [y+1, x], [y+1, x+2], [y+2, x+1]]

    def pentadecathlon(y, x):
        return [
            [y, x+1], [y+1, x], [y+1, x+2],
            [y+2, x+1], [y+3, x+1], [y+4, x+1],
            [y+5, x], [y+5, x+2], [y+6, x+1]
        ]


x = 40
y = 40
init = []
for i in range(x):
    for j in range(y):
        if (i%5 == 0 and j%5 == 0):
            init += Bestiary.blinker(i,j)

jeu = Jeu(x,y, Bestiary.pulsar(10, 10) + Bestiary.cube(10, 10) + Bestiary.cube(5, 5) + Bestiary.glider(20, 20))
while True:
    jeu.print()
    time.sleep(0.05)
    jeu.next()