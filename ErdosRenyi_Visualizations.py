#!/usr/bin/env python
# coding: utf-8

# In[10]:


load('NumericalSemigroup.sage') 
from sage.plot.scatter_plot import ScatterPlot
import pandas as pd 
from sage.plot.histogram import Histogram
import matplotlib as plt
plt.style.use('default')


# In[75]:


#look at ratio of "small elements" to size 
def wilf_check(frobSpec, genusSpec, genSpec, embedSpec, numTrials): 
    wilfR = []
    wilfL = []
    for i in range(numTrials): #for every set of generators, run this test
        if ((frobSpec[i] + 1 - genusSpec[i])/(frobSpec[i] + 1)) < 0: #check if negative! 
            print("NEGTIVE WILF RATIO")
            print(i)
            print(genSpec[i])
            break #complete break if true
        wilfL.append((frobSpec[i] + 1)) #store left side of wilf inequality
        wilfR.append((frobSpec[i] + 1 - genusSpec[i])*(embedSpec[i] + 1))#store right side of wilf inequality
    ratio = [] 
    #check if left and right side are equal 
    differences = []
    for j in range(numTrials): 
        differences.append(wilfR[j] - wilfL[j])
        if wilfL[j] == wilfR[j]: #if equal, then store true
            ratio.append(True)
        else:
            ratio.append(False)
            if wilfL[j] > wilfR[j]: #also if left is greater than right, print generators and values 
                print("Left side greater than right!!")
                print("Sides of ratio(L, R): ", wilfL[j], wilfR[j])
                print("Generators:", genSpec[j])
                print("Index:", j)
    difference_plot = list(zip(embedSpec, differences))
    w = scatter_plot(difference_plot, title = 'Wilf Difference between left and right')
    show(w)
    return(ratio)


# In[76]:


#given m, prefix, preefix for generators, and number of trials 
#looks at wilf ratio 
#produces histograms for all stored values (frobenius number, genus, generators, and embedding dim)
def readIn(m, prefix, prefixGen, numTrials):
    suffix = ".csv"
    
    name = prefix + suffix
    nameGens = prefixGen  + suffix
    nameGraph = prefix + "graphs" + suffix
    #import data from csv and assign name
    dfSpec = pd.read_csv(name) 
    embedSpec = list(dfSpec["embedSpec"])
    frobSpec = list(dfSpec["frobSpec"])
    genusSpec = list(dfSpec["genusSpec"])
    dfSpecgens = pd.read_csv(nameGens)
    genSpecTemp = dfSpecgens.to_numpy()
    genSpec = []
    #save all generators except 0, which is in every set of generators (m equivelence class after COL) 
    for i in range(numTrials):
        newList = [item for item in genSpecTemp[i]if not(math.isnan(item)) == True and item != 0]
        genSpec.append(newList)
    
    checks = wilf_check(frobSpec, genusSpec, genSpec, embedSpec, numTrials) #true for if equality achieved
    gensEqual = [] 
    for i in range(numTrials):
        if checks[i]: 
            gensEqual.append(genSpec[i])
    #print all sets of generators that produce equality
    print("Generators of equal Wilf's Ratio")
    print(gensEqual)
    
    #put all generators in long array instead of seperately (for easy histogram)
    allGens = []
    for g in genSpec:
        allGens.extend(g)
    #number of bins determined by the amount of unique values of each set of numbers
    a = histogram(allGens, bins = len(set(allGens)), title = 'Generators')
    b = histogram(frobSpec, bins = len(set(frobSpec)), title = 'Frobenius Number')
    c = histogram(genusSpec, bins = len(set(genusSpec)), title = 'Genus')
    d = histogram(embedSpec, bins = len(set(embedSpec)), title = 'Embedding Dimension')

    show(a)
    show(b)
    show(c)
    show(d)


# In[ ]:




