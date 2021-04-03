#!/usr/bin/env python
# coding: utf-8

# In[7]:


import numpy as np
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as Data
from torch.autograd import Variable

torch.cuda.set_device(0)

# 引入attribute向量
def get_data(feature_of_grid):
    feature_matrix = torch.from_numpy(feature_of_grid)
    torch_dataset = Data.TensorDataset(feature_matrix)
    data_loader = Data.DataLoader(dataset=torch_dataset, batch_size=128)
    return data_loader


# In[8]:


class AE(nn.Module):
    def __init__(self, input_dim, encoding_dim):
        super(AE, self).__init__()
        self.input_dim = input_dim
        self.encoding_dim = encoding_dim
        self.encoder = nn.Sequential(
                        nn.Linear(self.input_dim, 48),
                        nn.ReLU(),
                        nn.Linear(48, self.encoding_dim))
        self.decoder = nn.Sequential(
                        nn.Linear(self.encoding_dim, 48),
                        nn.ReLU(),
                        nn.Linear(48, self.input_dim))
    
    def forward(self, input):
        m = self.encoder(input)
        out = self.decoder(m)
        return m, out


# In[9]:


def l1_penalty(var):
    return torch.abs(var).sum()


input_dim = 370
encoding_dim = 32
model = AE(input_dim, encoding_dim)
    
def train():  
    save_path = "generateData/AE.pkl"
    lr = 0.001
    epoches = 20
    weight_decay = 1e-5

    train_data = get_data()
    loss_score = 100
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    if torch.cuda.is_available():
        model.cuda()
    for epoch in range(epoches):
        running_loss = 0.0
        for batch_idx, data in enumerate(train_data):
            inputs = Variable(data[0])
            if torch.cuda.is_available():
                inputs = inputs.cuda()
            optimizer.zero_grad()
            mid_reps, outputs = model(inputs)
            mse_loss = F.mse_loss(outputs, inputs)
            l1_reg = weight_decay*l1_penalty(mid_reps)
            loss = mse_loss + l1_reg
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            if batch_idx%10 == 9:
                print('Train Epoch: %d, Batch %d, loss:%.6f' % (epoch+1, (batch_idx+1)/10, running_loss/100))
                if save_path and running_loss<loss_score:
                    loss_score = running_loss
                    torch.save(model, save_path)
                    print("******Save model successful******")
                running_loss = 0.0
            
            
    print("Finished Training")

train()





