import json
from src.load.database import get_db, DBCollections
from src.load.raspador_catalogo import catalogo_df, clean_catalogo_df

def list_all():
    """
        Função que retorna as disciplinas no catálogo da ufabc
    """
    try:
        response = _get_collection().find()
        if response.explain()["executionStats"]["executionSuccess"]: # Procura nos Status se a operação deu Certo
            return response
    except Exception as e:
        raise e 

def find_by_apelido(apelido):
    """
        Função que retorna informações acerca da disciplina atravez do apelido
    """
    try:
        response = _get_collection().find_one({ "apelido": apelido })
        if response:
            return response
    except Exception as e:
        raise e

def find_by_sigla(sigla):
    """
        Função que retorna informações acerca da disciplina atravez da sigla
    """
    try:
        response = _get_collection().find_one({ "sigla": sigla })
        if response:
            return response
    except Exception as e:
        raise e

def insert_item(item):
    """
        Função que insere uma disciplina na Coleção de Disciplinas
    """
    try:
        response = _get_collection().insert_one(item)
        if response:
            return response
    except Exception as e:
        raise e

def insert_items(items):
    """
        Função que insere uma lista de disciplinas na Coleção Catalogo
    """
    try:
        response = _get_collection().insert_many(items)
        if response:
            return response
        raise Exception("Erro ao inserir Fretados")
    except Exception as e:
        raise e

def delete_all():
    """
        Função que remove as disciplinas da Coleção de catálogo
    """
    try:
        response = _get_collection().delete_many({})
        if response:
            return response
    except Exception as e:
        raise e

def populate_database():
    # deleta o conteúdo atual do banco
    delete_all()

    # get dataframe
    clean_df = clean_catalogo_df(catalogo_df)
    
    # preparando as tabelas para inseri-las elemento a elemento no banco
    catalogo_json = json.loads(clean_df.to_json(orient='records'))

    # inserção
    insert_items(catalogo_json)

# função privada dentro desse módulo
def _get_collection():
    """
        Função que retorna a coleção de Fretados
    """
    try:
        return get_db.get_collection(DBCollections.CATALOGO)
    except Exception as e:
        raise e

