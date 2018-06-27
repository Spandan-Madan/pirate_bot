from general_helper_functions import *

from gensim.scripts.glove2word2vec import glove2word2vec
glove_input_file = '../glove.840B.300d/glove.840B.300d.txt'
word2vec_output_file = 'glove_gensim.txt'
glove2word2vec(glove_input_file, word2vec_output_file)

from gensim.models import KeyedVectors
# load the Stanford GloVe model
filename = 'glove_gensim.txt'
model_gensim = KeyedVectors.load_word2vec_format(filename, binary=False)
# calculate: (king - man) + woman = ?
# result = model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1)
# print(result)

model_gensim['hello']

import torch
from torch.autograd import Variable
model = torch.load('fasttext_to_glove_model.pt')

fasttext_embedding = load_pickle('fasttext_embedding.pckl')

def show_closest(word,N):
    try:
        word_embed = fasttext_embedding[word]
    except:
        print('Not in vocab')
        return 0

    tensor_x=torch.from_numpy(word_embed).float()
    x = Variable(tensor_x).type(torch.FloatTensor)
    y_pred = model(x)

    y_pred_array = y_pred.data.numpy()
    most_sim = model_gensim.most_similar(positive=[y_pred_array],topn=N)
    return most_sim

show_closest('man',20)

model_gensim.most_similar(positive=[model_gensim['man']],topn=20)
