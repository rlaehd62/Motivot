from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from service import data_service as ds
from sentence_transformers import SentenceTransformer
from utility.data_handler import *

config_store = get_config_storage()
tensor_store = get_tensor_storage()
faq_store = get_faq_storage()

model = SentenceTransformer(config_store.model)
chatter = ds.initialize_data(model=model)
app = FastAPI(title='Motiverse Chatbot', version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get("/")
def index():
    return "Hello World!"

@app.get("/chat")
def chat(intent: int, query: str):
    response = chatter.get_response(intent, query)
    print(f'Q. {query}')
    print(response)
    return response

@app.get("/faq")
def faq(intent: int):
    response = chatter.get_faq_list(intent)
    return { "Intent": intent, "FAQ": response }