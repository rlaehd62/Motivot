import pandas as pd, os
from sentence_transformers import util
from utility.data_handler import *
config_store = get_config_storage()
faq_store = get_faq_storage()

def search_faq(intent: int):
    '''
    FAQ Storage를 기반으로 Intent와 일치하는 텍스트를 반환한다.
    
    '''
    try:
        response = faq_store.get(intent)
        return response
    
    except Exception as ex:
        print(ex)
        return [ ]

def search_for(origin, embeddings, k: int = 3, threshold: float = 0.85):
    '''
    Embeddings 중 Origin과 T% 이상 일치하는 문장 중 가장 유사한 K개에 대한 다음과 같은 데이터를 반환한다.
    '''
    try:
        scores = util.pytorch_cos_sim(origin, embeddings)[0]
        
        top_k_indices = scores.argsort(descending=True)[:k]
        top_k_scores = scores[top_k_indices]

        valid_indices = top_k_indices[top_k_scores >= threshold]
        valid_scores = top_k_scores[top_k_scores >= threshold]

        if len(valid_indices) == 0:
            return -1

        results = [(int(idx), float(score)) for idx, score in zip(valid_indices, valid_scores)]
        return results
    
    except Exception as e:
        # 예외 발생하면 비어있는 결과를 반환한다.
        print(f"Error: {e}")
        return -1