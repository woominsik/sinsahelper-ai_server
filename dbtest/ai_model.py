#from crawling_main3 import crawl_by_url
# import random
# def reference_by_url(url):
#     #review_list = crawl_by_url(url)
    
#     return [random.randint(1,101), random.randint(1,101), random.randint(1,101)]
from .crawling import crawl_by_url
from .BERT_model import ReviewClassification
#from crawling import crawl_by_url
#from BERT_model import ReviewClassification
from functools import lru_cache
from enum import Enum

import torch
import os
from kobert_tokenizer import KoBERTTokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model
import gluonnlp as nlp
import numpy as np

model_root_path = 'models'
max_len = 100
device = torch.device('cpu')

class Model_Type(Enum):
    SHIP = 0
    SIZE = 1
    QUALITY = 2


def reference_by_url(url):
   review_list = crawl_by_url(url)
   token_list, valid_length_list, segment_id_list = review2inputs(review_list)
   scores = calc_score(token_list, valid_length_list, segment_id_list)
   return scores

def review2inputs(review_list):
    tokenizer = load_tokenizer()
    vocab = load_vocab()
    transform = nlp.data.BERTSentenceTransform(
        tokenizer.tokenize,
        max_seq_length=max_len,
        vocab=vocab,
        pad=True,
        pair=False
    )
    token_list = []
    valid_length_list = []
    segment_id_list = []
    for review in review_list:
        text = ' '.join(review)
        sentence = transform([text])
        token_list.append(torch.LongTensor(np.array([sentence[0]])))
        valid_length_list.append(sentence[1])
        segment_id_list.append(torch.LongTensor(np.array([sentence[2]])))

    return token_list, valid_length_list, segment_id_list

def calc_score(token_list, valid_length_list, segment_id_list):
   max_value = len(token_list) * 1.5
   if max_value == 0:
    max_value = 1
   score_list = np.array([0., 0., 0.])
   for tokens, valid_length, segment_ids in zip(token_list, valid_length_list, segment_id_list):
      tokens = tokens.to(device)
      segment_ids = segment_ids.to(device)
      for i, model_type in enumerate(Model_Type):
         model = load_model(model_type)
         outputs = model(tokens, [valid_length], segment_ids)
         prob, predict = outputs.max(dim=1)
         score = prob.item() * predict.item()
         score_list[i] += score

   if score_list.max() > max_value:
      max_value = score_list.max()

   '''
   score_list = min_max_norm(score_list, max=max_value)
   score_list *= 100
   score_list = score_list.astype(np.int32)
   '''
   score_list /= max_value
   score_list *= 100
   score_list = score_list.astype(np.int32)

   return score_list.tolist()


def min_max_norm(data, min=0, max=100):
    data = (data-min) / (max-min)
    return data

@lru_cache
def load_model(model_type: Model_Type):
    model = ReviewClassification(3)
    if model_type == Model_Type.SHIP:
        model_path = os.path.join(model_root_path, 'ship.pt')
    elif model_type == Model_Type.SIZE:
        model_path = os.path.join(model_root_path, 'size.pt')
    elif model_type == Model_Type.QUALITY:
        model_path = os.path.join(model_root_path, 'quality.pt')
    else:
        raise RuntimeError('Not a valid model_type')
    
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    return model

@lru_cache
def load_tokenizer(key=0):
    return KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')

@lru_cache
def load_vocab(key=0):
    _, vocab = get_pytorch_kobert_model()
    return vocab