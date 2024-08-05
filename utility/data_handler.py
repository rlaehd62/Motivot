import json, pandas as pd
import torch, os, logging as lg

class config_storage:
    def __init__(self, config_file = "config.json"):
        self.map = self.__load_json__(config_file)
    
        
    def __load_json__(self, config_file):
        if not os.path.exists(config_file):
            print('No config.json found')
            exit(0)
            
        with open(config_file, 'r') as file:
            return json.load(file)    
        
    @property
    def intent(self): return self.map['intent']
    
    @property
    def query(self): return self.map['query']
    
    @property
    def queries(self): return self.map['queries']
    
    @property
    def answer(self): return self.map['answer']
    
    @property
    def data(self): return self.map['data']
    
    @property
    def dictionary(self): return self.map['dictionary']
    
    @property
    def data_folder(self): return self.map['data_folder']
    
    @property
    def model(self): return self.map['model']
    
    @property
    def faq(self): return self.map['faq']
    
    @property
    def faq_data(self): return self.map['faq_data']

_config_store = None
def get_config_storage():
    global _config_store
    if _config_store is None: _config_store = config_storage()
    return _config_store

class tensor_storage:
    '''
    Tensor 데이터를 관리하는 클래스 (Key-Value)
    '''
    
    def __init__(self):
        '''
        지정한 Folder 내의 모든 파일을 Tensor 데이터로 가정한다.\n
        Tensor 데이터를 로드한 뒤 파일의 이름을 KEY로 사용하여 등록한다.
        '''
        self.store = {}
        folder = _config_store.data_folder
        if not os.path.exists(folder): os.mkdir(folder)
    
    @staticmethod
    def is_embedded():
        '''
        텐서 폴더 내의 실제로 텐서 파일이 있는지 확인한다.
        이는 초기 실행되는 텐서 변환 과정을 다시 실행하지 않기 위함이다.
        '''
        folder = _config_store.data_folder
        if os.path.exists(folder) and len(os.listdir(folder)) > 0: return True  
        return False
    
    def load(self):
        folder = _config_store.data_folder
        files = os.listdir(folder)
        
        for file in files:
            file_name = file.split('.')[0]
            embedding = torch.load(f'{folder}/{file}')
            self.store[file_name] = embedding
    
    def get(self, key: str):
        '''
        KEY와 대응하는 Tensor 데이터를 반환한다.
        (해당 KEY가 존재하지 않을 시 프로그램을 종료한다)
        '''
        
        try:
            return self.store[key]
        except Exception as e:
            lg.critical(f'{key}와 대응하는 Tensor 데이터를 찾을 수 없습니다 (프로그램 종료)')
            print(e)
            return ""

_tensor_store = None
def get_tensor_storage():
    global _tensor_store
    if _tensor_store is None: _tensor_store = tensor_storage()
    return _tensor_store

class faq_storage:
    
    def __init__(self):
        self.store = self.__load__()
        print(self.store)
        
    def __load__(self):
        try:
            file: str = _config_store.faq_data
            if not os.path.exists(file): raise FileNotFoundError('FAQ Not Found!')
            df = pd.read_csv(file, keep_default_na=False)
            return df.groupby(_config_store.intent)[_config_store.faq].apply(list).to_dict()
        
        except Exception as ex:
            print(ex)
            return { "FAQ Not Found" }
    
    def get(self, key):
        try:
            message = self.store[key]
            print(f'FAQ [{key}] >> {message}')
            return self.store[key]
        
        except Exception as ex:
            print(ex)
            return []
        
_faq_storage = None
def get_faq_storage():
    global _faq_storage
    if _faq_storage is None: _faq_storage = faq_storage()
    return _faq_storage