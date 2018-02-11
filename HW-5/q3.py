#!/usr/bin/env python
###################################
# Name of the author: SHILPASHREE RAO
# Email id: shilpasr@usc.edu
#####################################
import distsim

# you may have to replace this line if it is too slow 
word_to_ccdict = distsim.load_contexts("nytcounts.4k")


### provide your answer below

print 'manhattan - name'
distsim.show_nearest(word_to_ccdict, word_to_ccdict['manhattan'],set(['manhattan']),distsim.cossim_sparse)
print 'island - common noun'
distsim.show_nearest(word_to_ccdict, word_to_ccdict['island'],set(['island']),distsim.cossim_sparse)
print 'annual - adjective'
distsim.show_nearest(word_to_ccdict, word_to_ccdict['annual'],set(['annual']),distsim.cossim_sparse)
print 'create - verb'
distsim.show_nearest(word_to_ccdict, word_to_ccdict['create'],set(['create']),distsim.cossim_sparse)
print 'investment - noun'
distsim.show_nearest(word_to_ccdict, word_to_ccdict['investment'],set(['investment']),distsim.cossim_sparse)
print 'e-mail - noun/verb'
distsim.show_nearest(word_to_ccdict, word_to_ccdict['e-mail'],set(['e-mail']),distsim.cossim_sparse)
print 'build'
distsim.show_nearest(word_to_ccdict, word_to_ccdict['build'],set(['build']),distsim.cossim_sparse)

###Answer examples
distsim.show_nearest(word_to_ccdict, word_to_ccdict['jack'],set(['jack']),distsim.cossim_sparse)

