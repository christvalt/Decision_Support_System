import os, numpy as np, pandas as pd, math
import PSO as ParSwarm
    
def compute_fitness(xvec, portfolioInitialValue, horizon, valoriDiforcast):
   # varaitioneIndice
    variation = [] 
    
    
    valorePortafoglio = [0] * horizon
    #rendimento o valore portafoglio finale =average ultimo mese(20 giorni(per il prof)) 
    media20giorni=rendimento = [0] * horizon#rendimento
    #rischio std.dev
    squareError = [0] * horizon#
    
    
    sigoloPortafoglio = []
    #print("len"+str(horizon))
    for i in range(len(xvec)):
        
       # print("valorerrrrrrrrrr"+str(len(valoriDiforcast)))
        #print("len"+str(horizon))
        sigoloPortafoglio.append([portfolioInitialValue*xvec[i]])
        #print("initial value for index"+str(sigoloPortafoglio[i]))
     #per ogni dimensione[i] ,per ogni giorno[j] faccio i segueti calcoli 
    for i in range(len(xvec)):
        variation.append([])
        for j in range(len(valoriDiforcast[i])):
            
           # print("test"+ str(j))
            #di quanto varia le mie indice di forcast in percentuale.same exel(B4-B3)/B4 code 
            #print("test*****"+str(variation))
            soum1=(valoriDiforcast[i][j]-valoriDiforcast[i][j-1])/valoriDiforcast[i][j-1]
            #print("dataframe"+str(soum1))
            variation[i].append(soum1) #[0,0]
            #print("test22" +str(variation[i][j]))
            #per ogni indice ,update il falore del suo portafoglion,
            #valeur pour son capital pour chaque jours 
            capital=(1+variation[i][j])*sigoloPortafoglio[i][j-1]
            #print("capital initial"+str(capital))
            sigoloPortafoglio[i].append(capital)
            #print("entered")
    
            #la somma portafoglio per le 7 dimenzione=portafoglio per un giorno
            #exel =SUM(R6:X6)
            valorePortafoglio[j] = valorePortafoglio[j] + sigoloPortafoglio[i][j]
            #print("resukr"+str(SomaPortfolio[0]))
                
           
    for i in range(19, horizon):
    #media della la somma delle ultime valori dei 20 ultimi giorni  valore del portafoglio finale
       media20giorni[i]= rendimento[i] = sum(valorePortafoglio[i-19:i]) / 20
       #print("rendimento".format(len(rendimento)))
       #
       #squareError[i] = valorePortafoglio[i] - rendimento[i]
       
       squareError[i] = (valorePortafoglio[i] - rendimento[i])*(valorePortafoglio[i] - rendimento[i])
       count=(horizon - 20)
       sommasquareerro=sum(squareError[19:])
       mediasqrError=sommasquareerro/count
    return_value =media20giorni[horizon - 1]
   #squareErrorAvg = sum(squareError[19:]) / (horizon - 20)
    if mediasqrError > 0:
        devst = math.sqrt(mediasqrError)
    else:
        devst = -1
    return return_value - devst, return_value, devst
