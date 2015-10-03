"""
Character level RNN using lasagne and theano.

@author: Merel Theisen and Tobias Rijken

example usage:
	python char_lstm.py <input_file>
"""

import lasagne
import numpy as np
import sys
import theano
import theano.tensor as T

from lasagne.layers import DenseLayer, InputLayer, LSTMLayer, SliceLayer

lasagne.random.set_rng(np.random.RandomState(1))

def preprocess(l, batch_size, seq_length, n_vocab, data, target, char_to_index):
	x = np.zeros((batch_size, seq_length, n_vocab))
	y = np.zeros(batch_size)

	for i in range(batch_size):
		ptr = i
		for j in range(seq_length):
			x[i, j, char_to_index[data[l+ptr+j]]] = 1.
			if target:
				y[i] = char_to_index[data[l+ptr+seq_length]]

	return x, np.array(y, dtype='int32')

def build_network(n_hidden, grad_clip, n_vocab):
	net = {}

	net['input'] = InputLayer(shape=(None, None, n_vocab))
	net['lstm_1'] = LSTMLayer(net['input'], n_hidden, \
		grad_clipping=grad_clip, nonlinearity=lasagne.nonlinearities.tanh)
	net['lstm_2'] = LSTMLayer(net['lstm_1'], n_hidden, \
		grad_clipping=grad_clip, nonlinearity=lasagne.nonlinearities.tanh)
	net['slice'] = SliceLayer(net['lstm_2'], -1, 1)
	net['out'] = DenseLayer(net['slice'], num_units=n_vocab, \
		W=lasagne.init.Normal(), nonlinearity=lasagne.nonlinearities.softmax)

	return net

def sample(probs, seq_length, batch_size, n_vocab, init_phrase, char_idx, ix_to_char, N=200):
	sample = []
	x, _ = preprocess(len(init_phrase)-seq_length, 1, seq_length, n_vocab, init_phrase, False, char_idx)

	for i in range(N):
		index = np.argmax(probs(x).ravel())
		sample.append(index)
		x[:,0:seq_length-1,:] = x[:,1:,:]
		x[:,seq_length-1,:] = 0
		x[0,seq_length-1,sample[-1]] = 1.

	random_snippet = init_phrase + ''.join(ix_to_char[idx] for idx in sample)    
	print "----\n {} \n----".format(random_snippet)


def main(file_name):
	# Set hyperparameters
	max_epochs = 50
	learning_rate = 2e-3
	seq_len = 20
	batch_size = 50
	grad_clip = 5
	n_hidden = 128
	print_freq = 100
	# phrase = "<!DOCTYPE html><html>"
	phrase = "The quick brown fox jumps"

	# Process data
	text = open(file_name, 'r').read()
	chars = list(set(text))
	n_data = len(text)
	n_vocab = len(chars)

	char_to_index = {ch:i for i,ch in enumerate(chars)}
	index_to_char = {i:ch for i,ch in enumerate(chars)}

	print "Building network..."
	net = build_network(n_hidden, grad_clip, n_vocab)

	targets = T.ivector('targets')
	net_out = lasagne.layers.get_output(net['out'])
	loss = lasagne.objectives.categorical_crossentropy(net_out, targets).mean()

	params = lasagne.layers.get_all_params(net['out'])

	updates = lasagne.updates.adagrad(loss, params, learning_rate)

	# Theano functions
	train = theano.function([net['input'].input_var, targets], loss, \
		updates=updates, allow_input_downcast=True)
	get_loss = theano.function([net['input'].input_var, targets], loss, \
		allow_input_downcast=True)
	probs = theano.function([net['input'].input_var], net_out, \
		allow_input_downcast=True)

	# Start training
	print "Start training..."

	l = 0
	for i in xrange(n_data * max_epochs / batch_size):
		sample(probs, seq_len, batch_size, n_vocab, phrase, char_to_index, index_to_char)


		avg_cost = 0
		for j in xrange(print_freq):
			x, y = preprocess(l, batch_size, seq_len, n_vocab, text, True, char_to_index)

			l += seq_len + batch_size - 1
			if (l + batch_size + seq_len) >= n_data:
				print "Reset"
				l = 0
			avg_cost += train(x,y)
		print "Epoch {}, average loss = {}".format(i*1.0*print_freq/n_data*batch_size, avg_cost / print_freq)

if __name__ == '__main__':
	main(sys.argv[1])