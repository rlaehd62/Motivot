import pandas as pd, time
from utility.data_handler import *
from preprocess.argumentation import KoreanEDA

print("# Load configuration from JSON ...")
config_store = get_config_storage()

print("OpenAI KEY: ", end='')
key = input()

print(f"Load dataframe from the file '{config_store.data}'")
raw_df = pd.read_csv(config_store.data, index_col=False, keep_default_na=False)
df = raw_df.drop_duplicates(subset=[config_store.intent, config_store.query])

eda = KoreanEDA(key)

print("Generating augmented sentences and intents for all sentences in the DataFrame...")
augmented_data = []

for index, row in df.iterrows():
    intent = row[config_store.intent]
    query = row[config_store.query]
    answer = row[ config_store.answer]
    print(f"{intent} / {query}")


    print(f"Processing: Intent: {intent}, Query: {query}")
    response = eda.argument(query)
    print(response)
    time.sleep(0.3)
    
    try:
        result = response['sentences']
        print(result)
        
        print("Generated sentences and intents:")
        for sent in result:
            print(f"{query} >> {sent}")
            augmented_data.append({
                config_store.intent: intent,
                config_store.query: sent,
                config_store.answer: answer
            })
    except Exception as ex:
        print(ex)

augmented_df = pd.DataFrame(augmented_data)
df.to_csv("backup.csv", index=False)
df = pd.concat([df, augmented_df], ignore_index=True)
print("Updated DataFrame:")
print(df)

df.to_csv(config_store.data, index=False)
print(f"DataFrame saved to '{config_store.data}'")
