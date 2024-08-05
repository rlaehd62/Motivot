import json
from openai import OpenAI

class KoreanEDA:
    '''
    데이터 증강 기능을 제공하는 클래스\n
    OpenAI GPT-3.5-Turbo를 통해서 입력된 텍스트를 증강한다.
    '''
    
    schema = {
        'type': 'object',
        'properties': {
            'sentences': {
                'type': 'array',
                'description': 'List of generated sentences.',
                'items': { 'type': 'string' }
             },
        }
    }
    
    prompt = """
    We're doing Data Augmentation for existing sentence to start NLP Research.
    Assuming a new perspective which is different from the existing input, Rephrase the existing input into three of different Korean sentences Using diverse words.
    But you have to keep the whole context of sentence to synchronize the meaning with the input.
    Input: "{}"
    """
    
    def __init__(self, key):
        '''
        OpenAI에서 발급된 KEY 입력
        '''
        self.client = OpenAI(api_key=key)
        
    def argument(self, sentence):
        '''
        Argumentation 적용할 문장을 입력
        '''
        response = self.client.chat.completions.create(
            model = "gpt-3.5-turbo-0125",
            messages= [ 
                       { 'role': 'system', 'content': "You're helpful Data Augmentation Tool for NLP, designed to print JSON" },
                       { 'role': 'user', 'content': f"{self.prompt.format(sentence)}" } 
                      ],
            max_tokens=300,
            functions=[{'name': 'set_argument', 'parameters': self.schema}],
            function_call={'name': 'set_argument'}
        )

        json_data = response.choices[0].message.function_call.arguments
        return json.loads(json_data)