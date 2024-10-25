#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
535526 Optimization Algorithms: HW1

This file implements some useful functions needed in the main SVRG/SGD workflow.

"""
import numpy as np
import matplotlib.pyplot as plt
import os
import torch
from torch import nn
import torch.nn.functional as F
from torchvision import transforms, datasets 
from torch.utils.data.sampler import Sampler
import matplotlib.pyplot as plt

def MNIST_dataset():
    if not os.path.isdir("data"):
        os.mkdir("data")
    # Download MNIST dataset and set the valset as the test test
    transform = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5,), (0.5,))])
    test_set = datasets.MNIST('data/MNIST', download=True, train=False, transform=transform)
    train_set = datasets.MNIST("data/MNIST", download=True, train=True, transform=transform)
    return train_set, test_set

def MNIST_nn_one_layer():
    #---------- Your Code (~10 lines) ----------
    # Configure the input and output size of MNIST and specify the NN model
    input_size = 784
    hidden_sizes = [64]
    output_size = 10

    model = nn.Sequential(
        nn.Linear(input_size, hidden_sizes[0]),
        nn.ReLU(),
        nn.Linear(hidden_sizes[0], output_size),
        nn.LogSoftmax(dim=1))
    
    #---------- End of Your Code ----------
    return model

def MNIST_logistic():
    # Create the nn model
    input_size = 784
    hidden_sizes = [128, 64]
    output_size = 10

    # The non-convex function (model) is Sequential function fron torch. Notice that we have implemented an activation function to make it non-convex
    model = nn.Sequential(
        nn.Linear(input_size, hidden_sizes[0]),
        nn.ReLU(),
        nn.Linear(hidden_sizes[0], hidden_sizes[1]),
        nn.ReLU(),
        nn.Linear(hidden_sizes[1], output_size),
        nn.LogSoftmax(dim=1))

    return model

def accuracy(yhat, labels):
    _, indices = yhat.max(1)
    return (indices == labels).sum().data.item() / float(len(labels))

    
class AverageCalculator():
    def __init__(self):
        self.reset() 
    
    def reset(self):
        self.count = 0
        self.sum = 0
        self.avg = 0
    
    def update(self, val, n=1):
        assert(n > 0)
        self.sum += val * n 
        self.count += n
        self.avg = self.sum / float(self.count)

def plot_train_stats(train_loss, val_loss, train_acc, val_acc, directory, acc_low=0):
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(8,6), sharey='row')
    axes[0][0].plot(np.array(train_loss))
    axes[0][0].set_title("Training Loss")
    axes[0][1].plot(np.array(val_loss))
    axes[0][1].set_title("Validation Loss")
    axes[1][0].plot(np.array(train_acc))
    axes[1][0].set_title("Training Accuracy")
    axes[1][0].set_ylim(acc_low, 1)
    axes[1][1].plot(np.array(val_acc))
    axes[1][1].set_title("Validation Accuracy")
    plt.tight_layout()
    plt.savefig(os.path.join(directory, 'train_stats.png'))
    plt.close()