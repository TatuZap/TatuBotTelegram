from src.fretados.fretados_raspador import tables_on_page, clean_bus_df
from ..database import get_db, DBCollections
from datetime import datetime

def contador_calendario():
    hoje = datetime.now()
    Q1_inicio = datetime(2022,2,14)
    Q1_fim = datetime(2022,5,20)
    Q2_inicio = datetime(2022,6,6)
    Q2_fim = datetime(2022,8,31)
    Q3_inicio = datetime(2022,9,19)
    Q3_fim = datetime(2022,12,16)
    try:
        if(hoje >= Q1_inicio and hoje<=Q1_fim):
            delta = ((Q1_fim) - datetime.now()).days
            print(f"Estamos durante o Q1, faltam {delta} dia(s) para acabar o quadrimestre")
        elif(hoje >= Q2_inicio and hoje <= Q2_fim):
            delta = ((Q2_fim) - datetime.now()).days
            print(f"Estamos durante o Q2, faltam {delta} dia(s) para acabar o quadrimestre")
        elif(hoje >= Q3_inicio and hoje <= Q3_fim):
            delta = ((Q3_fim) - datetime.now()).days
            print(f"Estamos durante o Q3, faltam {delta} dia(s) para acabar o quadrimestre")
        elif((hoje < Q1_inicio) or (hoje > Q1_fim and hoje < Q2_inicio) or( hoje > Q2_fim and hoje < Q3_inicio) or (hoje > Q3_fim)):
            delta = ((Q3_fim) - datetime.now()).days
            print("Estamos durante o recesso, aproveite.")
    except Exception as e:
        raise e

# contador_calendario(hoje = datetime.now(), Q1_inicio = datetime(2022,2,14),Q1_fim = datetime(2022,5,20),Q2_inicio = datetime(2022,6,6),
# Q2_fim = datetime(2022,8,31), Q3_inicio = datetime(2022,9,19),Q3_fim = datetime(2022,12,10))

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




