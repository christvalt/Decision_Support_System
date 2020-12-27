import os, numpy as np,pandas as pd
import PSO as ParSwarm



def paraboloid(xvec):
    sum = 0
    for i in range(len(xvec)):
        sum += np.power(xvec[i], 2)
    return sum;

def rosenbrock(xvec):
    sum = 0
    for i in range(len(xvec)):
        sum += 100 * np.power((xvec[i+1] - np.power(xvec[i], 2)), 2) + np.power((1 - xvec[i]), 2)
    return sum

def compute_fitness (id , xvec):
    res=0.0
    if(id==1):res=paraboloid(xvec)    
    if(id==2):res=paraboloid(xvec)    
    return res         

def gopso(id ,niter,popsize,nhood_size):
    res=np.inf 
    
    if(id==1):    
        print("parabloid")
        numvar=7
        xmin =0,5
        xmax=0,8
        
    if(id==2):    
        print("rasenbork")
        numvar=7
        xmin =0,5
        xmax=0,8
        #gopso(idfunc,niter,popsize,nhood_size)
        
         #run optimizzation algorithm
    PSO = ParSwarm.ParSwarmOpt(xmin, xmax)
    res = PSO.pso_solve(popsize,id , numvar, niter, nhood_size)
    return res;
    #print("test value is".format(numvar,popsize))
    
if __name__=="__main___":
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
        
    idfunc=1
    niter=100
    popsize=40
    nhood_size=10  
    
    gopso(idfunc,niter,popsize,nhood_size) 
   
    
    
        