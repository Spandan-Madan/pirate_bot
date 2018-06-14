import io
import numpy as np
from general_helper_functions import *


import pickle
f = open('fasttext_embedding.pckl','rb')
fasttext_embedding = pickle.load(f)
f.close()

import pickle
f = open('glove_embedding.pckl','rb')
glove_embedding = pickle.load(f)
f.close()


vocab_glove = list(glove_embedding.keys())
vocab_fasttext = list(fasttext_embedding.keys())



vocab = list(set(vocab_glove) & set(vocab_fasttext))

import random

# indices_all = list(range(len(vocab)))
# random.shuffle(indices_all)
# train_indices = indices_all[:int(0.8*len(indices_all))]
# test_indices = indices_all[int(0.8*len(indices_all)):]

# save_pickle(train_indices,'train_indices.pckl')
# save_pickle(test_indices,'test_indices.pckl')

train_indices = load_pickle('train_indices.pckl')
test_indices = load_pickle('test_indices.pckl')

len(vocab)

BATCH_SIZE = 500

import torch
from torch.autograd import Variable

def get_train_batch(BATCH_SIZE):
    X_train = np.zeros((500,300))
    Y_train = np.zeros((500,300))

    random.shuffle(train_indices)
    batch_idx = train_indices[:BATCH_SIZE]
    ct = 0
    for i in batch_idx:
        word = vocab[i]
        try:
            fasttext = fasttext_embedding[word]
            glove = glove_embedding[word]
        except:
#             not_found_in_both.append(word)
            continue
        X_train[ct] = fasttext
        Y_train[ct] = glove
        ct += 1

    tensor_y=torch.from_numpy(Y_train).long()
    tensor_x=torch.from_numpy(X_train).float()

    return tensor_x,tensor_y

losses=[]

D_in, H, D_out = 300, 400, 300

# x = Variable(tensor_x).type(torch.FloatTensor)
# y = Variable(tensor_y,requires_grad=False).type(torch.LongTensor)

## Model Specification ##
model = torch.nn.Sequential(
          torch.nn.Linear(D_in, H),
          torch.nn.ReLU(),
          torch.nn.Linear(H, D_out),
        )

# model.cuda()
loss_fn = torch.nn.MSELoss()

learning_rate = 1e-3
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
print("Iteration \t Loss")
for t in range(10001):
    tens_x,tens_y = get_train_batch(BATCH_SIZE)
    x = Variable(tens_x).type(torch.FloatTensor)
    y = Variable(tens_y).type(torch.FloatTensor)

    y_pred = model(x)

    loss = loss_fn(y_pred, y)
    if t%1000==0:
        print(t, loss.data.tolist())
        torch.save(model, 'fasttext_to_glove_model.pt')
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
