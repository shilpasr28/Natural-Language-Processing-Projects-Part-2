###################################
# Name of the author: SHILPASHREE RAO
# Email id: shilpasr@usc.edu
####################################
import numpy as np

def run_viterbi(emission_scores, trans_scores, start_scores, end_scores):

    """Run the Viterbi algorithm.

    N - number of tokens (length of sentence)
    L - number of labels

    As an input, you are given:
    - Emission scores, as an NxL array
    - Transition scores (Yp -> Yc), as an LxL array
    - Start transition scores (S -> Y), as an Lx1 array
    - End transition scores (Y -> E), as an Lx1 array

    You have to return a tuple (s,y), where:
    - s is the score of the best sequence
    - y is a size N array of integers representing the best sequence.
    
    """
    L = start_scores.shape[0]
    assert end_scores.shape[0] == L
    assert trans_scores.shape[0] == L
    assert trans_scores.shape[1] == L
    assert emission_scores.shape[1] == L
    N = emission_scores.shape[0]

    vitTable = np.zeros(shape=(L, N))
    
    vitTable[:,0] = emission_scores[0,:] + start_scores
    
    pointTable = np.zeros(shape=(L, N))
    for col in range(1, N):
        for row in range(L):
            compArray = np.add(trans_scores[:,row], vitTable[:,col-1])
            vitTable[row][col] = np.add(np.amax(compArray), emission_scores[col][row])
            pointTable[row][col] = np.argmax(compArray)
          
    forbestScore = np.add(vitTable[:,N-1], end_scores)
    bestScore = np.amax(forbestScore)
    bestScoreind = np.argmax(forbestScore)
    indPoint = int(bestScoreind)
    Seq = [indPoint]   
    for col in range(N-1, 0, -1):
        Seq.append(int(pointTable[indPoint][col]))
        indPoint = int(pointTable[indPoint][col])
    bestSeq = np.array(Seq)  
        
    return bestScore, bestSeq[::-1]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             