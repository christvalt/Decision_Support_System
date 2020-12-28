import numpy as np
import random as rnd
from fitnessPSO import compute_fitness

class Particle:
    def __init__(self,_ndim, nhood_size):
        self.fit = self.return_value = self.devst = self.fitnbest = self.fitbest = self.return_valuebest = self.devstbest = 0
        self.v = np.zeros(_ndim, dtype=np.float)
        self.x = np.zeros(_ndim, dtype=np.float)
        self.xbest = np.zeros(_ndim, dtype=np.float)#local best
        self.nxbest = np.zeros(_ndim, dtype=np.float)#global best
        self.nset = np.zeros(nhood_size, dtype=np.int)
        
class ParSwarmOpt:
    def __init__(self,_xmin,_xmax):
        #velocity coefficient 
        self.w = 0.25
        self.c1 = 1.7
        self.c2 = 2.0
        self.fitbest = np.inf
        self.return_valuebest = np.inf
        self.devstbest = np.inf
        self.xmin = _xmin
        self.xmax = _xmax
        
    def pso_solve(self, popsize, numvar, niter, nhood_size, portfolioInitialValue, horizon, valoriDiforcast):
        rnd.seed(550)
        self.xsolbest = np.zeros(numvar, dtype=np.float)
        #---------------inizialize popolazione 
        pop = []
        for i in range(popsize):
            p = Particle(numvar, nhood_size)
            pop.append(p)
            
        for i in range(popsize):
            # initialize  positions and velocities
            for j in range(numvar):
                pop[i].x = np.random.dirichlet(np.ones(numvar))
                pop[i].v = [(rnd.random() - rnd.random()) * \
                        0.5 * (self.xmax - self.xmin) - self.xmin] * numvar
                pop[i].xbest = pop[i].x
                pop[i].nxbest = pop[i].x
                
            # initialize  global and local fitness
            pop[i].fit, pop[i].return_value, pop[i].devst = compute_fitness(pop[i].x, portfolioInitialValue, horizon, valoriDiforcast)
            pop[i].fitbest = pop[i].fit
            pop[i].return_valuebest = pop[i].return_value
            pop[i].devstbest = pop[i].devst
            
            # initialize neighborhood
            for j in range(nhood_size):
                id = rnd.randrange(popsize)
                while (id in pop[i].nset):
                    id = rnd.randrange(popsize)
                else:
                    pop[i].nset[j] = id;
        #-------------------------------------------run the code niter volte
        for iter in range(niter):
            print("iteration  {0} zub {1}".format(iter, self.fitbest))
            # update all particle (una per volta)
            for i in range(popsize):
                # for each dimension
                for d in range(numvar):
                    # stochastic coefficients
                    rho1 = self.c1 * rnd.random()
                    rho2 = self.c2 * rnd.random()
                    
                    # update velocity
                    pop[i].v[d] = self.w * pop[i].v[d] + \
                        rho1 * (pop[i].xbest[d] - pop[i].x[d]) + \
                        rho2 * (pop[i].nxbest[d] - pop[i].x[d])
                    
                    # update position
                    pop[i].x[d] += pop[i].v[d]
                    
                    # clamp position within bound
                    if (pop[i].x[d] < self.xmin):
                        pop[i].x[d] = self.xmin
                        pop[i].v[d] = -pop[i].v[d]
                    elif (pop[i].x[d] > self.xmax):
                        pop[i].x[d] = self.xmax
                        pop[i].v[d] = -pop[i].v[d]
                        
                    # sum 1
                    pop[i].x = pop[i].x / sum(pop[i].x)
                                
                    for d2 in range(numvar):
                        # clamp position within bound after setting range 0-1
                        if (pop[i].x[d2] < self.xmin):
                            diff = self.xmin - pop[i].x[d2]
                            pop[i].x[d2] = self.xmin
                            max_index = np.where(pop[i].x == np.amax(pop[i].x))[0]
                            pop[i].x[max_index] -= diff
                        
                # update particle fitness
                pop[i].fit, pop[i].return_value, pop[i].devst = compute_fitness(pop[i].x, portfolioInitialValue, horizon, valoriDiforcast)
                
                #update personal best position, min
                if (pop[i].fit < pop[i].fitbest):
                    pop[i].fitbest = pop[i].fit
                    pop[i].return_valuebest = pop[i].return_value
                    pop[i].devstbest = pop[i].devst
                    for j in range(numvar):
                        pop[i].xbest[j] = pop[i].x[j]
                        
                # update neighborhood best
                pop[i].fitnbest = np.inf
                for j in range(nhood_size):
                    if (pop[pop[i].nset[j]].fit < pop[i].fitnbest):
                        pop[i].fitnbest = pop[pop[i].nset[j]].fit
                        # copy particle position to gbest vector
                        for k in range(numvar):
                            pop[i].nxbest[k] = pop[pop[i].nset[j]].x[k]
                       
                # update gbest
                if (pop[i].fit < self.fitbest):
                    # update best fitness
                    self.fitbest = pop[i].fit
                    self.return_valuebest = pop[i].return_value
                    self.devstbest = pop[i].devst
                    # copy particle pos to gbest vector
                    for j in range(numvar):
                        self.xsolbest[j] = pop[i].x[j]
                        
                        
                     
        return self;