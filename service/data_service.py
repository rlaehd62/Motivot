import pandas as pd
from utility import data_retriever as handler
from service.chat_service import Chatter
from preprocess.preprocess import Preprocess
from preprocess.embedding import CreateEmbeddingData
from sentence_transformers import SentenceTransformer
from utility.data_handler import *
config_store = get_config_storage()
tensor_store = get_tensor_storage()

def initialize_data(model: SentenceTransformer):
    
    query_col = config_store.query
    raw_df = pd.read_csv(config_store.data, index_col=False, keep_default_na=False)
    df = raw_df.drop_duplicates(subset=[query_col])
        
    if not tensor_storage.is_embedded():
        print("test")
        encoder = CreateEmbeddingData(df, model=model)
        encoder.create_embedding(True)
    tensor_store.load()
    chatter = Chatter(df, model)
    return chatter