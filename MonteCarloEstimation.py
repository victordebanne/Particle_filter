"""
Estimation de la position avec methode de Monte-Carlo
(filtre particulaire ?)
"""
from visionpath import Space, matrixify
import ALG
import matplotlib.pyplot as plt
import random as r
import math
M = None

while True : 
    S = Space(3)
    M = matrixify(S, 50, 50)
    if M[35][35] == 0 : 
        break
"""
while True : 
    #créé un espace avec A et B libres
    M = create_matrix(50, 50)
    random_islande(M, 40, 7, 0.7)
    if M[A[0]][A[1]] == 0 and M[B[0]][B[1]] == 0 : 
        break
"""

#plt.imshow(M)

def random():
    return r.gauss(0, 0.1)

class Agent():
    def __init__(self, position, orientation, real = False):
        self.position = position
        self.orientation = orientation #normalisé
        self.real = real
        self.captor = None
        
    def moove(self, distance):
        self.position[0] += self.orientation[0] * distance + random()
        self.position[1] += self.orientation[1] * distance + random()
        
    def turn(self, angle):
    
        angle = angle + r.gauss(0, 0.05)
    
        x = self.orientation[0]
        y = self.orientation[1]
    
        new_x = x * math.cos(angle) - y * math.sin(angle)
        new_y = x * math.sin(angle) + y * math.cos(angle)
    
        self.orientation = ALG.normalize([new_x, new_y])
        
        
    def measures(self):
        pas = ALG.mult(self.orientation, 1/100)
        i = 0
        etat = self.position
        etat[0] = min(49, max(0, self.position[0]))
        etat[1] = min(49, max(0, self.position[1]))
        while True : 
            if M[int(etat[0])][int(etat[1])] == 1:
                break
            etat = ALG.add(etat, pas)
            i += 1
        self.captor = i/100 + random()
    
class Simulation():
    def __init__(self):
        #créé 1000 agents avec des positions et des directions aléatoires
        self.size = 1000
        self.agents = [Agent([r.randint(0, 49), r.randint(0, 49)], ALG.normalize([r.uniform(-1, 1), r.uniform(-1,1)])) for i in range(self.size)]
        self.proba = [1/self.size for i in range(self.size)] #on associe a chaque agent une probabilité qu'il soit le bon (au départ, ils sont tous equiprobables)
        self.resample = [None for i in range(self.size)]
        
    def moove(self, distance):
        for i in range(self.size):
            self.agents[i].moove(distance)
            
    def turn(self, angle):
        for i in range(self.size):
            self.agents[i].turn(angle)
            
    def measures(self):
        for i in range(self.size):
            self.agents[i].measures()
            
    def check(self, real_measure):
        for i in range(self.size):
            self.proba[i] *= 1/(1 + (self.agents[i].captor - real_measure)**2) #si le capteur et la vraie mesure sont egales alors = 1 plus ils sont distants plus c'est égal à 0
    
        #normalisation
        total = sum(self.proba)
        
        for i in range(self.size):
            self.proba[i] /= total
            
    def gaussian_check(self, real_measure):
        for i in range(self.size):
            error = self.agents[i].captor - real_measure
            sig = 1
            self.proba[i] *= math.exp(- (error**2) / (2 * sig ** 2))
        
            
        #normalisation
        total = sum(self.proba)
        
        for i in range(self.size):
            self.proba[i] /= total 
            
    def resampling(self):
        #avec acceptation/rejet
        i = 0
        max_proba = max(self.proba)
        while i < self.size : 
            alpha = r.uniform(0, max_proba)
            toss = r.randint(0, self.size - 1)
            if alpha <= self.proba[toss] :
                x = int(self.agents[toss].position[0] + r.gauss(0, 0.1))
                y = int(self.agents[toss].position[1] + r.gauss(0, 0.1))
                
                dirx = self.agents[toss].orientation[0] + r.gauss(0, 0.1)
                diry = self.agents[toss].orientation[1] + r.gauss(0, 0.1)
                
                new_orientation = ALG.normalize([dirx, diry])
                new_position = [x, y]
                
                self.resample[i] = Agent(new_position, new_orientation)
                i += 1
            else : 
                pass
        
        for i in range(self.size):
            self.agents[i] = self.resample[i]
            self.proba[i] = 1/self.size
            
    def resampling2(self):
        #avec roulette
        for i in range(self.size):
            alpha = r.random()
            cumul = 0
            for j in range(self.size):
                cumul += self.proba[j]
                if alpha <= cumul :
                    x = self.agents[j].position[0] + r.gauss(0, 0.1)
                    y = self.agents[j].position[1] + r.gauss(0, 0.1)
                    
                    dirx = self.agents[j].orientation[0] + r.gauss(0, 0.1)
                    diry = self.agents[j].orientation[1] + r.gauss(0, 0.1)
                    
                    new_orientation = ALG.normalize([dirx, diry])
                    new_position = [x, y]
                    
                    self.resample[i] = Agent(new_position, new_orientation)
                    break
                    
        for i in range(self.size):
            self.agents[i] = self.resample[i]
            self.proba[i] = 1/self.size
            
    def resampling3(self):
        #avec roulette et injection de particules aléatoires pour eviter la dégénérescence
        for i in range(self.size):
            alpha = r.random()
            cumul = 0
            beta = r.random()
            if beta <= 0.05 : 
                self.resample[i] = Agent([r.randint(0, 49), r.randint(0, 49)], ALG.normalize([r.uniform(-1, 1), r.uniform(-1,1)]))
                continue
            for j in range(self.size):
                cumul += self.proba[j]
                if alpha <= cumul :
                    x = self.agents[j].position[0] + r.gauss(0, 0.1)
                    y = self.agents[j].position[1] + r.gauss(0, 0.1)
                    
                    dirx = self.agents[j].orientation[0] + r.gauss(0, 0.1)
                    diry = self.agents[j].orientation[1] + r.gauss(0, 0.1)
                    
                    new_orientation = ALG.normalize([dirx, diry])
                    new_position = [x, y]
                    
                    self.resample[i] = Agent(new_position, new_orientation)
                    break
                    
        for i in range(self.size):
            self.agents[i] = self.resample[i]
            self.proba[i] = 1/self.size
            
    def resampling4(self):
        #avec roulette et injection de particules aléatoires pour eviter la dégénérescence
        for i in range(self.size):
            alpha = r.random()
            cumul = 0
            beta = r.random()
            if beta <= 0.05 : 
                self.resample[i] = Agent([r.randint(0, 49), r.randint(0, 49)], ALG.normalize([r.uniform(-1, 1), r.uniform(-1,1)]))
                continue
            for j in range(self.size):
                cumul += self.proba[j]
                if alpha <= cumul :
                    k = 13
                    l = -5
                    sig_max = 1
                    sig =  sig_max/( 1 + 2**(k * self.proba[j] + l))
                    x = self.agents[j].position[0] + r.gauss(0, sig)
                    y = self.agents[j].position[1] + r.gauss(0, sig)
                    
                    dirx = self.agents[j].orientation[0] + r.gauss(0, sig)
                    diry = self.agents[j].orientation[1] + r.gauss(0, sig)
                    
                    new_orientation = ALG.normalize([dirx, diry])
                    new_position = [x, y]
                    
                    self.resample[i] = Agent(new_position, new_orientation)
                    break
                    
        for i in range(self.size):
            self.agents[i] = self.resample[i]
            self.proba[i] = 1/self.size
            
    def select(self, mode = 0):
        if mode == 0 : 
            #on prend la probabilité max. 
            agent = self.agents[self.proba.index(max(self.proba))]
            x = agent.position[0]
            y = agent.position[1]
            theta = agent.orientation
            
            return (x, y, theta)
            
        if mode == 1 : 
            #on prend la moyenne pondérée
            x = 0
            y = 0 
            thetax = 0
            thetay = 0
            for i in range(self.size):
                x += self.agents[i].position[0] * self.proba[i]
                y += self.agents[i].position[1] * self.proba[i]
                thetax += self.agents[i].orientation[0] * self.proba[i]
                thetay += self.agents[i].orientation[1] * self.proba[i]
                
            return (x, y, [thetax, thetay])
                
                
        
                
    def visualize(self):
        for i in range(self.size):
            x = self.agents[i].position[0]
            y = self.agents[i].position[1]
            plt.scatter(y, -x, s = self.proba[i] * 50)
        plt.xlim(0, 50)
        plt.ylim(-50, 0)
        plt.axis("equal")
        plt.show()
            
                 
        
A = Agent([35,35], [1, 0], True)

S = Simulation()

A.measures()

S.measures()
S.gaussian_check(A.captor)
S.visualize()


A.turn(1)
A.measures()

S.turn(1)
S.measures()
S.gaussian_check(A.captor)
S.visualize()
S.resampling4()

A.turn(1)
A.measures()

S.turn(1)
S.measures()
S.gaussian_check(A.captor)

S.visualize()


A.turn(1)
A.measures()

S.turn(1)
S.measures()
S.gaussian_check(A.captor)
S.resampling4()
S.visualize()

A.turn(1)
A.measures()

S.turn(1)
S.measures()
S.gaussian_check(A.captor)

S.visualize()

A.turn(1)
A.measures()

S.turn(1)
S.measures()
S.gaussian_check(A.captor)
S.resampling4()
S.visualize()

A.turn(1)
A.measures()

S.turn(1)
S.measures()
S.gaussian_check(A.captor)

S.visualize()

position1 = S.select(1)
x = int(position1[0])
y = int(position1[1])

position2 = S.select(0)
x2 = int(position2[0])
y2 = int(position2[1])



M[x][y] = 2
M[x2][y2] = 3
M[35][35] = 4

plt.imshow(M)
plt.show()
print(S.agents[S.proba.index(max(S.proba))].position)
print(S.agents[S.proba.index(max(S.proba))].orientation)
print(A.orientation)

    
        