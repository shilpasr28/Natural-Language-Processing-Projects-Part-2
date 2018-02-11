# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 08:32:20 2017

@author: SHILPASHREE RAO
"""
import sys
import distsim
import numpy as np
#from astropy.table import Table, Column


with open('word-test.v3.txt', 'r') as f:
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
            anlgyIn = each.strip('\t').split()      
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

        tp1 = (count1/float(tot))
        t1 = list(str(tp1))
        if t1[2]== '0':
            top1 = round(tp1, 3)
        else:
            top1 = round(tp1, 2)
        
        tp5 = (count5/float(tot))
        t5 = list(str(tp5))
        if t5[2]== '0':
            top5 = round(tp5, 3)
        else:
            top5 = round(tp5, 2)
            
        tp10 = (count10/float(tot))
        t10 = list(str(tp10))
        if t10[2]== '0':
            top10 = round(tp10, 3)
        else:
            top10 = round(tp10, 2)
            
        tupl = (sentence[0], top1, top5, top10)
        print tupl
#        rowList.append(tupl)
        
#    ResTable = Table(rows=rowList, names=('Group', '1-best', '5-best', '10-best'))
#    print ResTable




        
    

 
    
    
   
        
 

