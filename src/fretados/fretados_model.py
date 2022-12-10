from src.fretados.fretados_raspador import tables_on_page, clean_bus_df
from ..database import get_db, DBCollections

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

def next_bus(origem, destino, horario_solicitacao, horario_limite, dia_semana): # TODO
    """
        Função que retorna os próximos Fretados baseada na origem, destino, horário_partida e intervalo.
    Args:
        origem: Onde o usuário se encontra.
        destino: Onde o usuário deseja ir.
        horario_solicitacao: Quando exatamente ele fez essa requisição ?.
        horario_limite: Qual a carência permitida ?60 minutos é o padrão.
    Returns:
        Cursor (tipo iterável) do pymongo com a resposta, que pode ser vazia.
    """

    return _get_collection().find({
        "origem": origem,
        "destino": destino,
        "dias" : "SEMANA" if dia_semana < 5 else "SABADO",
        "hora_partida" : {"$gte" : horario_solicitacao, "$lt": horario_limite}
    })

def find_by_linha(linha, dia_semana):
    """
        Função que retorna todos os Fretados com base na linha
    """
    try:
        response = _get_collection().find_one({
            "linha": linha,
            "dias" : "SEMANA" if dia_semana < 5 else "SABADO"
        })
        if response:
            return response
    except Exception as e:
        raise e

def find_by_all_fields(linha ,origem, destino, hora_partida, hora_chegada, dias, desembarque_terminal_leste):
    """
        Função que retorna todos os fretados que satisfazem
        que possuem todos seus campos mapeados pela busca.
    """
    try:
        response = _get_collection().find({
            "linha" : linha,
            "origem" : origem,
            "destino" : destino,
            "hora_partida" : hora_partida,
            "hora_chegada" : hora_chegada,
            "dias" : dias,
            "desembarque_terminal_leste": desembarque_terminal_leste,
        }
        ).limit(1)
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
    fretados_dicts = parsed_dataframe.to_dict('records')

    # inserção
    insert_items(fretados_dicts)

# função privada dentro desse módulo
def _get_collection():
    """
        Função que retorna a coleção de Fretados
    """
    try:
        return get_db.get_collection(DBCollections.FRETADOS)
    except Exception as e:
        raise e

class Fretado:
    """
    Classe que Modela o Objeto de negócio Fretado
    - linha:                      O número da linha de onibus, pode ter valores de 1 a 6
    - dias:                       Pode ser de dois valores 'SEMANA' e 'SABADO'
    - origem:                     Pode ser de dois valores 'SA' e 'SBC'
    - hora_partida:               Pode ser do valor de um horário, tipo '8:25' ou 'N/A' caso não tenha valor
    - destino:                    Pode ser de dois valores 'SA' e 'SBC'
    - hora_chegada:               Pode ser do valor de um horário, tipo '8:25' ou 'N/A' caso não tenha valor
    - desembarque_terminal_leste: Caso tenha desembarque no Terminal Leste é o valor de um horário, tipo '8:25', caso contrário, 'N/A'
    """
    def __init__(self, linha, dias, origem, hora_partida, destino, hora_chegada, desembarque_terminal_leste) -> None:
        self.dias = dias
        self.origem = origem
        self.destino = destino
        self.hora_partida = hora_partida
        self.hora_chegada = hora_chegada
        self.linha = linha
        self.desembarque_terminal_leste = desembarque_terminal_leste

    def __str__(self) -> str:
        return "Fretado da Linha: {} que parte de {} as {} e chega em {} as {}, operando durante (o/a) {}".format(self.linha,self.origem,self.destino,self.hora_partida,self.hora_chegada,self.dias)

    def to_dict(self) -> dict:
        return self.__dict__

    def from_dict(dictionary):
        del dictionary['_id']

        return Fretado(**dictionary)
