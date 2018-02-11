# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 17:50:03 2017

@author: SHILPASHREE RAO
"""

import argparse # optparse is deprecated
from itertools import islice # slicing for iterators
 
def word_matches(h, ref):
    return sum(1 for w in h if w in ref)
 
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
        rset = set(ref)
        h1_match = word_matches(h1, rset)
        h2_match = word_matches(h2, rset)
        a1 = 0.80
        a2 = 0.80
        
        if h1_match == 0:
            h1_l = 0
        else:            
            h1_precision = float(h1_match)/len(h1)
            h1_recall = float(h1_match)/len(rset)        
            h1_l = float(h1_precision*h1_recall)/((1-a1)*h1_recall + a1*h1_precision)
        
        if h2_match == 0:
            h2_l = 0
        else:
            h2_precision = float(h2_match)/len(h2)
            h2_recall = float(h2_match)/len(rset)
            h2_l = float(h2_precision*h2_recall)/((1-a2)*h2_recall + a2*h2_precision)
                
        print(1 if h1_l > h2_l else # \begin{cases}
                (0 if h1_l == h2_l
                    else -1)) # \end{cases}
# convention to allow import of this file as a module
if __name__ == '__main__':
    main()
