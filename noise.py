import random
import time

CHARS = " .:-=+*#%@"

def map(taille_grille_x, taille_grille_y):
    counter = 0
    map = [[CHARS[0] for j in range(taille_grille_y)] for i in range(taille_grille_x)]
    pos = [taille_grille_x//2, taille_grille_y//2]
    map[pos[0]][pos[1]] = CHARS[-1]

    while(counter < (taille_grille_x*taille_grille_y)/2):
        _, new_pos = calc_prochain(pos, map)
        new_char = CHARS[calc_moyenne(pos, map)]
        pos = new_pos
        map[pos[0]][pos[1]] = new_char
        counter += 1
    return map

def calc_moyenne(pos, map):
    return max(min(CHARS.index(map[pos[0]][pos[1]]) + random.randint(-1,1), len(CHARS) - 1),0)


def calc_prochain(pos, map):
    direction = [random.randint(-1, 1), random.randint(-1, 1)]
    new_pos = [pos[0] + direction[0], pos[1] + direction[1]]
    while((direction[0] == 0 and direction[1] == 0) or new_pos[0] < 0 or new_pos[0] >= len(map) or new_pos[1] < 0 or new_pos[1] >= len(map[0])):
        direction = [random.randint(-1, 1), random.randint(-1, 1)]
        new_pos = [pos[0] + direction[0], pos[1] + direction[1]]

    return direction,new_pos

def afficher_grille(grille):
    for row in grille:
        print("".join(row))

def smooth_dark(x,y,map):
    voisins = []
    for i in range(max(0,x-1),min(len(map),x+2)):
        for j in range(max(0,y-1),min(len(map[i]),y+2)):
            ind = CHARS.index(map[i][j])
            voisins.append(ind)
    return CHARS[max(sum(voisins)//len(voisins),CHARS.index(map[x][y]))]

def smooth(x,y,map):
    voisins = []
    for i in range(max(0,x-1),min(len(map),x+2)):
        for j in range(max(0,y-1),min(len(map[i]),y+2)):
            ind = CHARS.index(map[i][j])
            voisins.append(ind)
    return CHARS[sum(voisins)//len(voisins)]

def clean(map, method=smooth):
    for i in range(len(map)):
        for j in range(len(map[i])):
            map[i][j] = method(i,j,map)

    return map

seed = random.randint(0,2000)
random.seed(seed)
afficher_grille(map(20,40))
random.seed(seed)
print("---------------------------------")
afficher_grille(clean(map(20, 40)))
random.seed(seed)
print("---------------------------------")
afficher_grille(clean(map(20, 40), smooth_dark))