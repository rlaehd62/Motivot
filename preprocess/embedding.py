# create_embedding_data.py
import torch, pandas as pd
from tqdm import tqdm
from .preprocess import Preprocess
from sentence_transformers import SentenceTransformer
from utility.data_handler import *
config_store = get_config_storage()

tqdm.pandas()

class CreateEmbeddingData:
    """
    텍스트 데이터를 임베딩 데이터로 변환하는 클래스입니다.
    """
    def __init__(self, df: pd.DataFrame, model: SentenceTransformer):
        """
        preprocess: Preprocess 객체 (선택적)
        df: 임베딩을 생성할 텍스트 데이터가 있는 pandas DataFrame
        """
        
        self.df = df
        self.p = Preprocess(config_store.dictionary) 
        self.model = model
        self.folder = config_store.data_folder
        
    def __get_intents__(self, df: pd.DataFrame):
        '''
        CSV 데이터 내에 존재하는 모든 종류의 Intent를 반환한다.
        '''
        intent_col = config_store.intent
        intents = list(set(df[intent_col].to_list()))
        return intents

    def create_embedding(self, do_preprocess=True):
        """
        DataFrame의 각 텍스트를 임베딩으로 변환하고, 이를 저장합니다.
        do_preprocess: 전처리를 수행할지 여부를 결정하는 불리언 값
        """
        
        if do_preprocess and self.p is None: raise ValueError("전처리를 수행하려면 Preprocess 객체가 필요합니다.")
        elif tensor_storage.is_embedded(): 
            print("다시 임베딩을 진행하시려면 데이터 폴더를 삭제해주세요!") 
            return
        
        questions_list = list(self.df[config_store.query])
        
        intent_col = config_store.intent
        query_col = config_store.query
        
        intent_list = self.__get_intents__(self.df)
        print(f'Intent List: {intent_list}')
        
        for intent in intent_list:
            questions_list = self.df[self.df[intent_col] == intent][query_col].to_list()
            self.__do_embedding__(intent, questions_list, do_preprocess)
            
        print("Embedding 작업이 성공적으로 종료됐습니다.")
        
    def __do_embedding__(self, intent, questions, do_preprocess):
        '''
        Intent와 Question을 받아 임베딩 작업을 수행하는 함수.
        결과 값은 없으며 {intent}.pt 형태의 임베딩 파일이 생성된다.
        '''
        
        for i in tqdm(range(len(questions)), desc=f"Processing Data in {intent}"):
            sentence = questions[i]
            if do_preprocess: questions[i] = self.p.process(sentence)
        embeddings = self.model.encode(questions)
        embedding_data = torch.from_numpy(embeddings)
        torch.save(embedding_data, f'{self.folder}/{intent}.pt')
    