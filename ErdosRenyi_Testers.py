#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import numpy as np
import math
import pandas as pd 


# In[2]:


def er_COL(m, prob, inc): #increments via multiplication
    i = 0
    j = m+1
    gens = [None]*m #empty set to hold all the numbers chosen
    if inc == 0: #if no inc specified, choose randomly from geometric probability
        while None in gens: #runs until there are m chosen numbers
            for i in range(m):
                x = np.random.geometric(prob) #chooses random occurrance from geometric probability
                gens[i] = x*m + i #fill each mod class 
    #if inc specified, simulate geometric probability with weighted coin
    elif inc > 1: #for inc >1, we increase by multiplying
        while None in gens: 
            #for every number >m, flips weighted coin 
            x = random.random() #generates random float less than 1       
            if x < prob: #simulates a weighted coin flip (has p probability of being true)
                gens[i] = j*m+i #fill the apery set
                i += 1
            if j%m == 0 and prob < 1: #every m numbers, multiply the probabilty by inc
                prob *= inc
                if prob > 1: #after probability surpases 1, we cap it at 1
                    prob = 1
            j += 1
    else: #for inc less than 1, we increaese by adding in exactly the same way as multiplying
        while None in gens: 
            x = random.random()        
            if x < prob:
                gens[i] = j*m+i
                i += 1
            if j%m == 0 and prob < 1:
                prob += inc
                if prob > 1: 
                    prob = 1
            j += 1
    
    origAP, minAP = AperySetCOL(m, gens)#send m chosen numbers to Circle of Lights, returns the Apery set and minimal members of apery set 
    return(origAP, minAP)
            


# In[3]:


def AperySetCOL(m, setOfn): #minor alteration to COL alorithm from INSERT
    Q = [0] 
    a = [math.inf]*m
    a[0] = 0
    minA = []
    isItMinimal = [False]*m
    for n in setOfn: 
        if m != n: 
            isItMinimal[n%m] = True #let all the generators be minimal except m
    while len(Q) > 0:
        n = Q.pop(0)
        if n <= a[n%m]:
            for g in setOfn: 
                if n > 0 and (n + g) <= a[(n+g)%m]:
                        isItMinimal[(n+g)%m] = False #if we can define n in terms of others, it is not minimal
                if (n + g) < a[(n+g)%m]:
                    a[(n+g)%m] = (n + g)
                    Q.append(n + g)
    for r in range(len(a)):
        if isItMinimal[r]: #from boolean isItMinimal, we store only the minimal members of the Apery set (the generators)
            minA.append(a[r])
    return(a, minA) #returns Apery set, and minimal members of Apery
        


# In[4]:


def massTesting(m, inc, prob, numTrials): 
    specRandArray, frobNumsSpecArray, embedSpecArray, genusSpecArray = [None]*numTrials, [None]*numTrials, [None]*numTrials, [None]*numTrials
    #store (generators, frobenius number, embedding dimension, and genus) at corresponding indecies
    randGens = [0]
    for j1 in range(numTrials): #runs user specified # trials for specific m, p, and inc values
        randGens = [0]
        while len(randGens) < 3: #runs until greater than 3 generators (for Wilf's purpose)
            origAp, randGens = er_COL(m, prob, inc)
        frobNumsSpecArray[j1] = max(origAp) - m  #calculate frobenius number for random generators from aperey set
        specRandArray[j1] = randGens #store random generators
        origApK = [ num // m for num in origAp] #each generator can be written as m*k + i, new array stores k values
        genusSpecArray[j1] = sum(origApK)  #calculate genus for random generators from k values
        embedSpecArray[j1] = len(randGens) #store embedding dimension for ease of access
        j1 += 1
    
    return(frobNumsSpecArray, genusSpecArray, embedSpecArray, specRandArray)


# In[14]:


#increment, probability, and number of trials are all optional parameters, if not passed, assigned
def testHome(m, prefix, prefixGen, prefixConst, inc = 0, prob = (0.6-random.uniform(0,0.6))/10, numTrials = 10000): 
    suffix = ".csv" 
    name = prefix + suffix #takes user specified prefix, creates csv name for all values except the generators
    nameGens = prefixGen + suffix #takes user specified prefix, creates csv name for generators
    nameConst = prefixConst + suffix #takes user specified prefix, creates csv name for generators

    frobNumsSpecArray, genusSpecArray, embedSpecArray, specRandArray = massTesting(m, inc, prob, numTrials)

    dfSpec = pd.DataFrame({'embedSpec':embedSpecArray, 'frobSpec': frobNumsSpecArray,
               'genusSpec': genusSpecArray})
    dfSpec.to_csv(name, index=False)
    dfSpecGens = pd.DataFrame(specRandArray) #generators needed to be stored seperately because of pandas
    dfSpecGens.to_csv(nameGens, index=False)
    dfSpecConst = pd.DataFrame({'inc':inc, 'prob': prob, 'numTrials': numTrials}, index = [0])
    dfSpecConst.to_csv(nameConst, index = False)


# In[ ]:





# In[ ]:




