"""

"""

import cPickle
import lasagne
import numpy as np
import sys
import theano

BATCH_SIZE = 128
in_text = ""

def gen_data(p, char_to_ix, batch_size = BATCH_SIZE, data = in_text, SEQ_LENGTH = 20, vocab_size=500, return_target=True):
	x = np.zeros((batch_size,SEQ_LENGTH,vocab_size))
	y = np.zeros(batch_size)

	for n in range(batch_size):
		ptr = n
		for i in range(SEQ_LENGTH):
			x[n,i,char_to_ix[data[p+ptr+i]]] = 1.
		if(return_target):
			y[n] = char_to_ix[data[p+ptr+SEQ_LENGTH]]
	return x, np.array(y,dtype='int32')

def main(file_name, N=1000):
	with open(file_name, "r") as f:
		net_list = cPickle.load(f)

	probs = net_list[0]
	network_output = net_list[1]
	cost = net_list[2]
	all_params = net_list[3]
	l_out = net_list[4]
	l_forward_slice = net_list[5]
	l_forward_1 = net_list[6]
	l_forward_2 = net_list[7]
	l_in = net_list[8]
	seq_len = net_list[9]
	ix_to_char = net_list[10]
	char_to_ix = net_list[11]
	vocab_size = net_list[12]
	batch_size = net_list[13]

	phrase = "<!DOCTYPE html><html>"

	x,_ = gen_data(len(phrase)-seq_len, char_to_ix, 1, phrase, seq_len, vocab_size, 0)
	sample_ix = []

	for i in range(N):
		# Pick the character that got assigned the highest probability
		ix = np.argmax(probs(x).ravel())
		# Alternatively, to sample from the distribution instead:
		# ix = np.random.choice(np.arange(vocab_size), p=probs(x).ravel())
		sample_ix.append(ix)
		x[:,0:seq_len-1,:] = x[:,1:,:]
		x[:,seq_len-1,:] = 0
		x[0,seq_len-1,sample_ix[-1]] = 1. 

	random_snippet = phrase + ''.join(ix_to_char[ix] for ix in sample_ix)    
	print("----\n %s \n----" % random_snippet)



if __name__ == '__main__':
	main(sys.argv[1])