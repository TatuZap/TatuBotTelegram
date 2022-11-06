import json
from src.load.database import get_db, DBCollections
from src.load.raspador_fretados import tables_on_page, clean_bus_df

def list_all():
    """
        Função que retorna todos os Fretados da coleção de Fretados
    """
    try:
        response = _get_collection().find()
        if response.explain()["executionStats"]["executionSuccess"]: # Procura nos Status se a operação deu Certo
            return response
    except Exception as e:
        raise e 

def next_bus(origem, destino, horario): # TODO
    """
        Função que retorna os próximos Fretados baseada na origem, destino e no horário.
    """
    return _get_collection().find({ "origem": origem, "destino": destino }) # TODO hour comparison

def find_by_linha(linha):
    """
        Função que retorna todos os Fretados com base na linha
    """
    try:
        response = _get_collection().find_one({ "linha": linha })
        if response:
            return response
    except Exception as e:
        raise e

def insert_item(item):
    """
        Função que insere um Fretado na Coleção de Fretados
    """
    try:
        response = _get_collection().insert_one(item)
        if response:
            return response
    except Exception as e:
        raise e

def insert_items(items):
    """
        Função que insere uma lista de Fretados na Coleção de Fretados
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
        Função que remove todas as entradas da coleção de fretados
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
    parsed_dataframe = clean_bus_df(tables_on_page)

    # preparando as tabelas para inseri-las elemento a elemento no banco
    fretados_json = json.loads(parsed_dataframe.to_json(orient='records'))

    # inserção
    insert_items(fretados_json)

# função privada dentro desse módulo
def _get_collection():
    """
        Função que retorna a coleção de Fretados
    """
    try:
        return get_db.get_collection(DBCollections.FRETADOS)
    except Exception as e:
        raise e
class FretadosModel:
    """
    Classe que Modela o Objeto de negócio Fretado
    - dias:            Pode ser de dois valores 'SEMANA' e 'SABADO'
    - origem:          Pode ser de dois valores 'SA' e 'SBC'
    - destino:         Pode ser de dois valores 'SA' e 'SBC'
    - hora_partida:    Pode ser do valor de um horário, tipo '8:25' ou 'N/A' caso não tenha valor
    - hora_chegada:    Pode ser do valor de um horário, tipo '8:25' ou 'N/A' caso não tenha valor
    - linha:           O número da linha de onibus, pode ter valores de 1 a 6
    """
    def __init__(self, dias, origem, destino, hora_partida, hora_chegada, linha) -> None:
        self.dias = dias 
        self.origem = origem 
        self.destino = destino 
        self.hora_partida = hora_partida
        self.hora_chegada = hora_chegada
        self.linha = linha
    
    def __str__(self) -> str:
        return "Fretado da Linha: {} que parte de {} as {} e chega em {} as {}, operando durante (o/a) {}".format(self.linha,self.origem,self.destino,self.hora_partida,self.hora_chegada,self.dias)
