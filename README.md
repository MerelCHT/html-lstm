# html-lstm
The aim of this project is to create a LSTM recurrent neural network that can learn to generate webpages character by character consisting of HTML and CSS. 
The network is trained on a text file with HTML and CSS that has been taken from random urls. The pages to which the urls lead did not or hardly use any JavaScript. 
..

## Training

The model was trained on an Amazon AWS g2.2x GPU instance as follows:
```
THEANO_FLAGS='floatX=float32,device=gpu0,nvcc.fastmath=True' python lstm_test.py
```

## Future directions
Ideally this project could be used towards the higher goal of generating personalised web pages. So for example, a specific website will look differently depending on which user is accessing it and what her/his web preferences are. This means that we would also need to pass some features of the user to the model. One can image that someone who is more visually oriented, sees webpages with more graphical content, whereas someone else might get a website with more text. However, it is unlikely that such an approach will use a character-level model.

A second interesting direction in the realm of e-commerce is the use of reinforcement learning to optimise the structure of a website for an individual to maximise the future return (or revenue) from that customer.

## Results
Examples can be found in 
```example_output1.html``` and ```example_output2.html```
