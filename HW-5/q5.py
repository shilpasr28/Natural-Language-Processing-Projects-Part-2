#!/usr/bin/env python
###################################
# Name of the author: SHILPASHREE RAO
# Email id: shilpasr@usc.edu
####################################
import distsim
word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")
###Provide your answer below

###Answer examples
print 'jack-example'
distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['jack'],set(['jack']),distsim.cossim_dense)
print 'manhattan - name'
distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['manhattan'],set(['manhattan']),distsim.cossim_dense)
print 'island - common noun'
distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['island'],set(['island']),distsim.cossim_dense)
print 'annual - adjective'
distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['annual'],set(['annual']),distsim.cossim_dense)
print 'create - verb'
distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['create'],set(['create']),distsim.cossim_dense)
print 'investment - noun'
distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['investment'],set(['investment']),distsim.cossim_dense)
print 'e-mail - noun/verb'
distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['e-mail'],set(['e-mail']),distsim.cossim_dense)
print 'build'
distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['build'],set(['build']),distsim.cossim_dense)
