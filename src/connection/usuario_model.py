import json
from src.connection.database import DBconfig, get_db, DBCollections
from src.connection.raspador_fretados import tables_on_page, clean_bus_df

def list_all():
    """
        Função que retorna todos os usuários
    """
    try:
        response = _get_collection().find()
        if response.explain()["executionStats"]["executionSuccess"]: # Procura nos Status se a operação deu Certo
            return response
    except Exception as e:
        raise e 


def find_by_id(id):
    """
        Função que retorna um usuário com base na no seu id único
    """
    try:
        response = _get_collection().find_one({ "id": id })
        if response:
            return response
    except Exception as e:
        raise e

def find_and_update(id, ra):
    """
        Função que retorna um usuário com base na no seu id único
    """
    try:
        response = _get_collection().update_one({ "id": id }, { "$set": { "ra" : ra } } )
        if response:
            return response
    except Exception as e:
        raise e

def insert_item(item):
    """
        Função que insere um usuário na Coleção de usuários
    """
    try:
        response = _get_collection().insert_one(item)
        if response:
            return response
    except Exception as e:
        raise e

def insert_items(items):
    """
        Função que insere uma lista de usuários na Coleção dos usuários
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
        Função que remove todas as entradas da Coleção de usuário
    """
    try:
        response = _get_collection().delete_many({})
        if response:
            return response
    except Exception as e:
        raise e

# função privada dentro desse módulo
def _get_collection():
    """
        Função que retorna a Coleção de usuários
    """
    try:
        return get_db.get_collection(DBCollections.USUARIO)
    except Exception as e:
        raise e

class Usuario:
    """
        Um usuário possui um identificar único e possivelmente um RA.
    """
    def __init__(self, id, ra=None) -> None:
        self. id = id 
        self.ra = ra
    
    def __str__(self) -> str:
        return "Usuário: {}".format(self.id)
