import json
import src.connection.raspador_restaurante as raspador_restaurante
import pandas as pd 
from src.connection.database import get_db, DBCollections
from src.connection.raspador_restaurante import tables_on_page, clean_restaurant_df

def list_all():
    """
        Função que retorna todos os Restaurante da coleção de Restaurante
    """
    try:
        response = _get_collection().find()
        if response.explain()["executionStats"]["executionSuccess"]: # Procura nos Status se a operação deu Certo
            return response
    except Exception as e:
        raise e 

def insert_item(item):
    """
        Função que insere um Fretado na Coleção de Restaurante
    """
    try:
        response = _get_collection().insert_one(item)
        if response:
            return response
    except Exception as e:
        raise e

def find_by_weekday_str(data, complete_info=0):
    """
        Função que retorna informações acerca do almoço ou janta do RU
        Args: 
        data em forma de string dia/mes
        complete_info é um inteiro que possui valores entre 0 e 2 
        0 -> Almoço e janta
        1 -> Somente Almoço 
        2 -> Somente Janta 
    """
    try:
        if complete_info == 0 :
            response = _get_collection().find({ "data": data })
        elif complete_info == 1:
            response = _get_collection().find({ "data": data }, {"jantar" : 0})
        else: 
            response = _get_collection().find({ "data": data }, {"almoço" : 0})
        if response:
            return response
    except Exception as e:
        raise e

def find_by_weekday_num(dia_semana, complete_info=0):
    """
        Função que retorna informações acerca do almoço ou janta do RU
        Args: 
        dia_semana é um numero de 0  a 6 (segunda a domingo)
        complete_info é um inteiro que possui valores entre 0 e 2 
        0 -> Almoço e janta
        1 -> Somente Almoço 
        2 -> Somente Janta 
    """
    try:
        if complete_info == 0 :
            response = _get_collection().find({ "dia_semana": dia_semana })
        elif complete_info == 1:
            response = _get_collection().find({ "dia_semana": dia_semana }, {"jantar" : 0})
        else: 
            response = _get_collection().find({ "dia_semana": dia_semana }, {"almoço" : 0 })
        if response:
            return response
    except Exception as e:
        raise e


def insert_items(items):
    """
        Função que insere uma lista de Restaurante na Coleção de Restaurante
    """
    try:
        response = _get_collection().insert_many(items)
        if response:
            return response
        raise Exception("Erro ao inserir Restaurante")
    except Exception as e:
        raise e

def delete_all():
    """
        Função que remove todas as entradas da coleção de Restaurante
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
    parsed_dataframe = raspador_restaurante.clean_restaurant_df(raspador_restaurante.tables_on_page)

    # preparando as tabelas para inseri-las elemento a elemento no banco
    Restaurante_json = json.loads(parsed_dataframe.to_json(orient='records'))

    # inserção
    insert_items(Restaurante_json)

# função privada dentro desse módulo
def _get_collection():
    """
        Função que retorna a coleção de Restaurante
    """
    try:
        return get_db.get_collection(DBCollections.RESTAURANTE)
    except Exception as e:
        raise e





