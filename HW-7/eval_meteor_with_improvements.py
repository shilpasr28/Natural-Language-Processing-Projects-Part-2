# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 20:12:13 2017

@author: SHILPASHREE RAO
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 17:50:03 2017

@author: SHILPASHREE RAO
"""
import sys
import math
import nltk
import numpy as np
import string
import re
import argparse # optparse is deprecated
from itertools import islice # slicing for iterators
from collections import Counter
 
def word_matches(h, ref):
    return sum(1 for w in h if w in ref)

def consecutiveArray(pros, refpros):
    array = []
    for x in pros:
        if x in refpros:
            array.append(refpros.index(x))
    cons_array = np.split(array, np.where(np.diff(array) != 1)[0]+1)
    
    return cons_array

def bleu(cons_array, h_match, h_pros, refb_pros):
    gm2_1 = 0
    gm3_1 = 0
    gm4_1 = 0
    
    for x in cons_array:
        if len(x) > 1:
            gm2_1 += (len(x)-1)
        if len(x) > 2:
            gm3_1 += (len(x)-2)
        if len(x) >= 4:
            gm4_1 += (len(x)-3)         
            
    if gm2_1 == 0 or gm3_1 == 0 or gm4_1 == 0:
        Bleu = 0
    else:       
        geom = ((((float(h_match))/(len(h_pros))) * ((float(gm2_1))/((len(h_pros))-1)) 
        * ((float(gm3_1))/((len(h_pros))-2)) * ((float(gm4_1))/((len(h_pros))-3))) ** 0.25)

        if len(h_pros) > len(refb_pros):
            BP = 1
        else:
            BP = math.exp(1-(float(len(h_pros))/len(refb_pros)))
                    
        Bleu = BP * geom

    return  Bleu
               
def meteor(match, pros, rsetm, a, refm_pros, consm_array):
    if match == 0:
        meteor = 0
    else:            
        precision = float(match)/len(pros)
        recall = float(match)/len(rsetm)        
        Fscore = float(precision*recall)/((1-a)*recall + a*precision)
        chunk = len(consm_array)
        Penalty = 0.5 * (float(chunk) / match)
        meteor = Fscore * (1-Penalty) 
        
    return meteor


def cosinesim(h_pros, refc_pros):
    vector1 = Counter(h_pros)
    vector2 = Counter(refc_pros) 
    comp1 = set(vector1.keys()) 
    comp2 = set(vector2.keys())
    common = comp1 & comp2
    vecn = []
    vecda = []
    vecdb = []
    for i in common:
        vecn.append(vector1[i] * vector2[i])
    numr = sum(vecn)
    
    for i in vector1.keys():
        vecda.append(vector1[i]**2 )       
    denomA = sum(vecda)
    
    for i in vector2.keys():
        vecdb.append(vector2[i]**2 )       
    denomB = sum(vecdb)

    denr = math.sqrt(denomA) * math.sqrt(denomB)

    if denr == 0:
        return 0
    else:
        return float(numr) / denr
    
def main():
    parser = argparse.ArgumentParser(description='Evaluate translation hypotheses.')
    parser.add_argument('-i', '--input', default='data/hyp1-hyp2-ref',
            help='input file (default data/hyp1-hyp2-ref)')
    parser.add_argument('-n', '--num_sentences', default=None, type=int,
            help='Number of hypothesis pairs to evaluate')
    # note that if x == [1, 2, 3], then x[:None] == x[:] == x (copy); no need for sys.maxint
    opts = parser.parse_args()
 
    # we create a generator and avoid loading all sentences into a list
    def sentences():
        with open(opts.input) as f:
            for pair in f:
                yield [sentence.strip().split() for sentence in pair.split(' ||| ')]
    
 
    # note: the -n option does not work in the original code
    for h1, h2, ref in islice(sentences(), opts.num_sentences):
        h1_p1 = ' '.join(h1).lower()
        h1_p2 = map(lambda x:x.strip(string.punctuation),h1_p1.split(" "))
        h1_pros = (re.sub(r"\'s", " is", ' '.join(h1_p2))).split()
        
        h2_p1 = ' '.join(h2).lower()
        h2_p2 = map(lambda x:x.strip(string.punctuation),h2_p1.split(" "))
        h2_pros = (re.sub(r"\'s", " is", ' '.join(h2_p2))).split()
        
        ref_p1 = ' '.join(ref).lower()
        ref_p2 = map(lambda x:x.strip(string.punctuation),ref_p1.split(" "))
        ref_pros = (re.sub(r"\'s", " is", ' '.join(ref_p2))).split()

        rset = set(ref_pros)
        h1_match = word_matches(h1_pros, rset)
        h2_match = word_matches(h2_pros, rset)
        a1 = 0.80
        a2 = 0.80

###consecutive array for meteor and bleu##           
        consec1_array = consecutiveArray(h1_pros, ref_pros)
        consec2_array = consecutiveArray(h2_pros, ref_pros)  
        
###meteor##
        if h1_match == 0:
            h1_meteor = 0
        else:
            h1_meteor = meteor(h1_match, h1_pros, rset, a1, ref_pros, consec1_array)
           
####cosine similarity###
        cosineSim1 = cosinesim(h1_pros, ref_pros)
        
###POS Tagging###         
        tag1 = nltk.pos_tag(h1_pros)
        tag_1 = []
        for i in tag1:
            tag_1.append(i[1])
            
        tagr = nltk.pos_tag(ref_pros)
        tag_r = []
        for i in tagr:
            tag_r.append(i[1])
            
        pos1Match = word_matches(tag_1, tag_r)
        if pos1Match == 0:
            Pos1Blue = 0
        else:            
            Cons1Posarray = consecutiveArray(tag_1, tag_r)
            Pos1Blue = bleu(Cons1Posarray, pos1Match, tag_1, tag_r)
            setRef1 = set(tag_r)
            Pos1Meteor = meteor(pos1Match, tag_1, setRef1, a1, tag_r, Cons1Posarray)
        
###BLEU##
        if h1_match == 0:
            Bleu_1 = 0
        else:                        
            Bleu_1 = bleu(consec1_array, h1_match, h1_pros, ref_pros)
                      
        h1_l = ((0.7 * h1_meteor) + (0.25 * Pos1Blue) + (0 * Pos1Meteor) + (0 * Bleu_1) + (0.05 * cosineSim1))
        
###meteor##
        if h2_match == 0:
            h2_meteor = 0
        else:
            h2_meteor = meteor(h2_match, h2_pros, rset, a2, ref_pros, consec2_array)
            
####cosine similarity###
        cosineSim2 = cosinesim(h2_pros, ref_pros)
            
###POS Tagging###         
        tag2 = nltk.pos_tag(h2_pros)
        tag_2 = []
        for i in tag2:
            tag_2.append(i[1])

        pos2Match = word_matches(tag_2, tag_r)
        if pos2Match == 0:
            Pos2Blue = 0
        else:
            Cons2Posarray = consecutiveArray(tag_2, tag_r)
            setRef2 = set(tag_r)
            Pos2Meteor = meteor(pos2Match, tag_2, setRef2, a2, tag_r, Cons2Posarray)
            Pos2Blue = bleu(Cons2Posarray, pos2Match, tag_2, tag_r)
                        
###BLEU##
        if h2_match == 0:
            Bleu_2 = 0
        else:                        
            Bleu_2 = bleu(consec2_array, h2_match, h2_pros, ref_pros)
                      
        h2_l = ((0.7 * h2_meteor) + (0.25 * Pos2Blue) + (0 * Pos2Meteor) + (0 * Bleu_2) + (0.05 * cosineSim2))         
                
        print(1 if h1_l > h2_l else # \begin{cases}
                (0 if h1_l == h2_l
                    else -1)) # \end{cases}
# convention to allow import of this file as a module
if __name__ == '__main__':
    main()