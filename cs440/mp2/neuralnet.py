# neuralnet.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/29/2019
# Modified by Mahir Morshed for the spring 2021 semester

"""
This is the main entry point for MP3. You should only modify code
within this file and neuralnet_part2.py -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class NeuralNet(nn.Module):
    def __init__(self, lrate, loss_fn, in_size, out_size):
        """
        Initializes the layers of your neural network.
        
        @param lrate: learning rate for the model
        @param loss_fn: A loss function defined as follows:
            @param yhat - an (N,out_size) Tensor
            @param y - an (N,) Tensor
            @return l(x,y) an () Tensor that is the mean loss
        @param in_size: input dimension
        @param out_size: output dimension

        For Part 1 the network should have the following architecture (in terms of hidden units):

        in_size -> 32 ->  out_size

        We recommend setting lrate to 0.01 for part 1.

        """
        super(NeuralNet, self).__init__()
        self.loss_fn = loss_fn
        self.lrate = lrate
        self.in_size = in_size 
        self.out_size = out_size

        hidden = 32
        self.model = nn.Sequential(nn.Linear(in_size, hidden),
                            nn.ReLU(),
                            nn.Linear(hidden, out_size))

        self.optimizer = optim.SGD(self.model.parameters(), lr=lrate, momentum = 0.9)    
        #self.optimizer = optim.Adam(self.model.parameters(), lr=lrate)                    

  

    def forward(self, x):
        """Performs a forward pass through your neural net (evaluates f(x)).

        @param x: an (N, in_size) Tensor
        @return y: an (N, out_size) Tensor of output from the network
        """
        
        return  self.model(x)

    def step(self, x, y):
        """
        Performs one gradient step through a batch of data x with labels y.

        @param x: an (N, in_size) Tensor
        @param y: an (N,) Tensor
        @return L: total empirical risk (mean of losses) at this timestep as a float
        """
        
        self.optimizer.zero_grad()

        loss = self.loss_fn(self.forward(x), y)

        
        loss.backward() 

        self.optimizer.step()

        return loss.item()


def fit(train_set, train_labels, dev_set, n_iter, batch_size=100):
    """ Make NeuralNet object 'net' and use net.step() to train a neural net
    and net(x) to evaluate the neural net.

    @param train_set: an (N, in_size) Tensor
    @param train_labels: an (N,) Tensor
    @param dev_set: an (M,) Tensor
    @param n_iter: an int, the number of iterations of training
    @param batch_size: size of each batch to train on. (default 100)

    This method _must_ work for arbitrary M and N.

    @return losses: array of total loss at the beginning and after each iteration.
            Ensure that len(losses) == n_iter.
    @return yhats: an (M,) NumPy array of binary labels for dev_set
    @return net: a NeuralNet object
    """
    losses = []
    yhats = []
    mean = torch.mean(train_set, dim = 0)
    std = torch.std(train_set,dim = 0) 
    
    train_set = (train_set - mean)/std
    dev_set = (dev_set - mean)/std

    
    batches = torch.split(train_set, batch_size)
    label_split = torch.split(train_labels, batch_size)

    net = NeuralNet(0.00058, nn.CrossEntropyLoss(), train_set.shape[1], 2) 


    for i in range(n_iter):
        losses.append(net.step(batches[i%(len(batches))], label_split[i%(len(label_split))]))

    for image in dev_set:
        yhat = net.model(image)
        if yhat[0] > yhat[1]:
            yhats.append(0)
        else:
            yhats.append(1)
    return losses, yhats, net