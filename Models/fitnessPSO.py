import os, numpy as np, pandas as pd, json, math
import PSO as ParSwarm
    
def compute_fitness(xvec, portfolioInitialValue, horizon, result_forecasts):
    variation = [[0]] * len(xvec)
    
    totalPortfolio = [0] * horizon
    average20days = [0] * horizon
    squareError = [0] * horizon
    
    portfolioValues = []
    for i in range(len(xvec)):
        portfolioValues.append([portfolioInitialValue*xvec[i]])
    
    for i in range(len(xvec)):
        for j in range(0,len(result_forecasts[i])):
            if j > 0:
                #update variation
                variation[i].append((result_forecasts[i][j]-result_forecasts[i][j-1])/result_forecasts[i][j-1])
                #update portfolio for each index
                portfolioValues[i].append((1+variation[i][j])*portfolioValues[i][j-1])
                #sum portfolios for each iteration
            totalPortfolio[j] = totalPortfolio[j] + portfolioValues[i][j]
           
    for i in range(19, horizon):
       average20days[i] = sum(totalPortfolio[i-19:i]) / 20
       squareError[i] = totalPortfolio[i] - average20days[i]
       
    return_value = squareError[horizon - 1]
    squareErrorAvg = sum(squareError[19:]) / (horizon - 20)
    if squareErrorAvg > 0:
        devst = math.sqrt(squareErrorAvg)
    else:
        devst = -1
    return return_value - devst, return_value, devst