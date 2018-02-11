# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 08:32:20 2017

@author: SHILPASHREE RAO
"""
from __future__ import division
import sys
import distsim
import numpy as np
#from astropy.table import Table, Column


with open('word-test-Q8.txt', 'r') as f:
    rowList = []
#    ResTable = Table()
    text = (f.read()).split(':')
    for i in text[1:]:
        tot = 0
        count1 = 0
        count5 = 0
        count10 = 0
        
        sentence = i.splitlines()
        Flag = False

        for each in sentence[1:]:
            tot += 1 
            word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")
            anlgyIn = each.split()          
            w1 = word_to_vec_dict[anlgyIn[0]]
            w2 = word_to_vec_dict[anlgyIn[1]]
            w4 = word_to_vec_dict[anlgyIn[3]]
            ret = distsim.show_nearest(word_to_vec_dict, w1-w2+w4, \
                                       set([anlgyIn[0], anlgyIn[1], anlgyIn[3]]),
                                       distsim.cossim_dense)
            List1 = [anlgyIn[0], anlgyIn[1], anlgyIn[2], anlgyIn[3]]
            List2 = [anlgyIn[0], anlgyIn[1], ret[0][0], anlgyIn[3]]

            
            if Flag == False:
                if List1[2] != List2[2]:
                    insert = List2[2]
                else:
                    for tup in ret[1:9]:
                        if tup[0] != List1[2]:
                            insert = tup[0]
                            break
                print sentence[0]
                print("Actual = {} : {} :: {} : {}".format(anlgyIn[0], anlgyIn[1], anlgyIn[2], anlgyIn[3]))
                print("Wrongly Predicted = {} : {} :: {} : {}".format(anlgyIn[0], anlgyIn[1], insert, anlgyIn[3]))
                print ''
            Flag = True           
            if List1[2] == List2[2]:
                count1 += 1
            for tup in ret[0:4]:
                if tup[0] == anlgyIn[2]:
                    count5 += 1
            for tup in ret[0:]:
                if tup[0] == anlgyIn[2]:
                    count10 += 1 
        top1 = (count1/tot)*100
        top5 = (count5/tot)*100
        top10 = (count10/tot)*100
        tupl = (sentence[0], top1, top5, top10)
        print tupl
#        rowList.append(tupl)

#    ResTable = Table(rows=rowList, names=('Group', '1-best', '5-best', '10-best'))
#    print ResTable
        



        
    

 
    
    
   
        
 

