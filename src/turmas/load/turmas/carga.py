import json
import os
#Carrega todos os arquivos da pasta output no banco
#files = file_output
sep = '\\' if os.name == 'nt' else '/'
def load_json(get_db,file_output):
    for path in file_output():
        file_name = path.split(sep)[-1]
        colletion = get_db[file_name]
        file = open(path)
        file_json = json.load(file)['data']
        colletion.insert_many(file_json)

def load_one(get_db,data,collection_name):
    try:
        collection = get_db[collection_name]
        file = open(data)
        file_json = json.load(file)
        collection.insert_many(file_json)
        print("successful data loading")
    except Exception as error:
        raise error
    