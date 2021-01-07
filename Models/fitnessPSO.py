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
   
        sigoloPortafoglio.append([portfolioInitialValue*xvec[i]])
     #per ogni dimensione[i] ,per ogni giorno[j] faccio i segueti calcoli 
    for i in range(len(xvec)):
        variation.append([])
        for j in range(len(valoriDiforcast[i])):
            
            #di quanto varia le mie indice di forcast in percentuale.same exel(B4-B3)/B4 code 
            soum1=(valoriDiforcast[i][j]-valoriDiforcast[i][j-1])/valoriDiforcast[i][j-1]
            variation[i].append(soum1) #[0,0]
            #per ogni indice ,update il falore del suo portafoglion,
            # valori per i caitale per ogni giorno 
            capital=(1+variation[i][j])*sigoloPortafoglio[i][j-1]
            sigoloPortafoglio[i].append(capital)
        
    
            #la somma portafoglio per le 7 dimenzione=portafoglio per un giorno
            #exel =SUM(R6:X6)
            valorePortafoglio[j] = valorePortafoglio[j] + sigoloPortafoglio[i][j]
                
           
    for i in range(19, horizon):
    #media della la somma delle ultime valori dei 20 ultimi giorni  valore del portafoglio finale
       media20giorni[i]= rendimento[i] = sum(valorePortafoglio[i-19:i]) / 20
       squareError[i] = valorePortafoglio[i] - rendimento[i]
       
      # squareError[i] = (valorePortafoglio[i] - rendimento[i])*(valorePortafoglio[i] - rendimento[i])
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
