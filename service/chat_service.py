import pandas as pd
from utility.data_retriever import search_for, search_faq
from preprocess.preprocess import Preprocess
from sentence_transformers import SentenceTransformer
from utility.data_handler import *
config_store = get_config_storage()
tensor_store = get_tensor_storage()

class Chatter:
    '''
    Chatbot에 관련된 질의응답, FAQ 기능을 모두 제공한다.
    단, 데이터의 검색 등은 Data Retriever에 의존하며 텐서의 검색은 Tensor Storage에 의존한다.
    '''
    def __init__(self, df: pd.DataFrame, model: SentenceTransformer):
        self.df = df
        self.model = model
        self.pp = Preprocess(config_store.dictionary)
        
    def __encode__(self, message):
        '''
        사용자의 질의를 빠르게 변환하기 위해서 텐서로 변환한다 (직접 X)
        '''
        return torch.tensor(self.model.encode(message))
    
    def get_faq_list(self, intent: int):
        '''
        Intent와 대응하는 FAQ 리스트를 제공한다.
        '''
        try:
            response = search_faq(intent)
            return response
    
        except Exception as ex:
            print(ex)
            return [ ]
    
    def get_response(self, intent: int, query: str, amount = 3):
        '''
        질문에 가장 적합한 정답을 최대 K개 반환한다.
        '''
        response = {}
        try:
            pass
            sentence = self.pp.process(query)
            print(f'{query} >> {sentence}')
            
            encoded_query = self.__encode__(sentence)
            encoded_data = tensor_store.get(f'{intent}')
            
            top_elements = search_for(encoded_query, encoded_data, k=amount) 
            if top_elements == -1: raise RuntimeError('Elements Not Found!') 
            print(f'Top-K elements retrieved: {top_elements}')
            
            best_idx = top_elements[0][0]
            
            intent_col = config_store.intent
            query_col = config_store.query
            answer_col = config_store.answer
            
            questions = list(self.df[self.df[intent_col] == intent][query_col])
            answers = list(self.df[self.df[intent_col] == intent][answer_col])
            
            response['Status'] = 404 if best_idx < 0 else 200
            response[config_store.intent] = intent  
            
            queries: list = []
            for element in top_elements:
                queries.append({
                    'query': questions[element[0]],
                    'answer': answers[element[0]],
                    'similarity': element[1]
                })
            response[config_store.queries] = queries
        
        except Exception as ex: 
            response['Status'] = 404
            response['Message'] = 'Nothing found in the server'
            print(ex)
            
        return response