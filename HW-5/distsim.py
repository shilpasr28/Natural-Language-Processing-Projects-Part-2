###################################
# Name of the author: SHILPASHREE RAO
# Email id: shilpasr@usc.edu
#####################################
import sys,json,math
import os
import numpy as np
from math import sqrt

def load_word2vec(filename):
    
    w2vec={}
    with open(filename,"r") as f_in:
        for line in f_in:
            line_split=line.replace("\n","").split()
            w=line_split[0]
            vec=np.array([float(x) for x in line_split[1:]])
            w2vec[w]=vec
    return w2vec

def load_contexts(filename):

    data = {}
    for word,ccdict in stream_contexts(filename):
        data[word] = ccdict
    print "file %s has contexts for %s words" % (filename, len(data))
    return data

def stream_contexts(filename):
    for line in open(filename):
        word, n, ccdict = line.split("\t")
        n = int(n)
        ccdict = json.loads(ccdict)
        yield word, ccdict

def cossim_sparse(v1,v2):
    valv1 =  v1.values()
    valv2 =  v2.values()
    numList = []
    denominatrX = (sqrt(sum([each*each for each in valv1])))
    denominatrY = (sqrt(sum([each*each for each in valv2])))
    for wordv1 in v1:
        for wordv2 in v2:
            if wordv1 == wordv2:                
                numList.append((v1[wordv1])*(v2[wordv2]))
    numerator = sum(numList)
    cosSim = (numerator/float((denominatrX)*(denominatrY))) 
    return cosSim


def cossim_dense(v1,v2):

    numerator = np.sum(np.multiply(v1, v2))
    denominatrX = np.sqrt(np.dot(v1, v1))
    denominatrY = np.sqrt(np.dot(v2, v2))
    resArray = np.divide(numerator, (np.multiply(denominatrX, denominatrY)))
    return resArray
    pass

def jaccard(v1,v2):

    numerator = np.sum(np.minimum(v1, v2))
    denominatr = np.sum(np.maximum(v1, v2))
    resArray = np.divide(numerator, denominatr)
    return resArray
    pass

def dice(v1,v2):

    numerator = (np.sum(np.minimum(v1, v2)))
    num = 2 * numerator
    denominatr = v1+v2
    den = np.sum(denominatr)
    resArray = np.divide(num, den)
    return resArray
    pass

def show_nearest(word_2_vec, w_vec, exclude_w, sim_metric):
       
    if (sim_metric.func_name == 'cossim_dense'):
        resList = []
        for word in word_2_vec:
            if word not in exclude_w:            
                array = word_2_vec[word]
                resList.extend([(word, cossim_dense(array, w_vec))])
                resList = sorted(resList, key= lambda x: x[1], reverse = True)
                if (len(resList) > 10):
                    resList.pop(-1)
                    
    elif(sim_metric.func_name == 'jaccard'):
        resList = []
        for word in word_2_vec:
            if word not in exclude_w:            
                array = word_2_vec[word]
                resList.extend([(word, jaccard(array, w_vec))])
                resList = sorted(resList, key= lambda x: x[1], reverse = True)
                if (len(resList) > 10):
                    resList.pop(-1)
                    
    elif(sim_metric.func_name == 'dice'):
        resList = []
        for word in word_2_vec:
            if word not in exclude_w:            
                array = word_2_vec[word]
                resList.extend([(word, dice(array, w_vec))])
                resList = sorted(resList, key= lambda x: x[1], reverse = True)
                if (len(resList) > 10):
                    resList.pop(-1)               
                    
    else: 
        resList = []
        for word in word_2_vec:
            if word not in exclude_w:
                vector = word_2_vec[word]
                resList.extend([(word, cossim_sparse(vector, w_vec))])
                resList = sorted(resList, key= lambda x: x[1], reverse = True)
                if (len(resList) > 10):
                    resList.pop(-1)  

 
    return resList
    pass

