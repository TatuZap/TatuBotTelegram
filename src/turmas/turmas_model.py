import src.turmas.turmas_ingressantes_raspador as turmas_ingressantes_raspador
import src.turmas.turmas_veteranos_raspador as turmas_veteranos_raspador
import src.turmas.turmas_pos_reajuste as turmas_pos_ajuste
import src.turmas.turmas_pos_ajuste_raspador as turmas_pos_reajuste_raspador
from ..database import get_db, DBCollections
from copy import deepcopy


def insert_items_SALAS_HORARIOS(items):
    """
        Função que insere um documentos relacionados a turmas na coleção de turmas
    """
    try:
        response = _get_collection_SALAS_HORARIOS().insert_many(items)
        if response:
            return response
        raise Exception("Erro ao inserir Turmas e Salas")
    except Exception as e:
        raise e

def insert_items_RA_TURMAS(items):
    """
        Função que insere um documentos relacionados a turmas na coleção de turmas
    """
    try:
        response = _get_collection_RA_TURMAS().insert_many(items)
        if response:
            return response
        raise Exception("Erro ao inserir Turmas")
    except Exception as e:
        raise e


def delete_all():
    """
        Função que remove todas os documentos relacionados com turmas
    """
    try:
        _get_collection_RA_TURMAS().delete_many({})
        _get_collection_SALAS_HORARIOS().delete_many({})
    except Exception as e:
        raise e

def populate_database():
    # deleta o conteúdo atual do banco
    delete_all()

    parsed_dataframe = turmas_veteranos_raspador.clean_turmas_salas_horarios_df(turmas_veteranos_raspador.df)
    turmas_dicts = parsed_dataframe.to_dict('records')
    insert_items_SALAS_HORARIOS(turmas_dicts)

    parsed_dataframe = turmas_ingressantes_raspador.clean_turmas_ingressantes_df(turmas_ingressantes_raspador.df)
    turmas_dicts = parsed_dataframe.to_dict('records')
    insert_items_RA_TURMAS(turmas_dicts)

    parsed_dataframe = turmas_pos_ajuste.clean_turmas_pos_ajuste_df(turmas_pos_ajuste.df)
    turmas_dicts = parsed_dataframe.to_dict('records')
    insert_items_RA_TURMAS(turmas_dicts)

    parsed_dataframe = turmas_pos_reajuste_raspador.clean_turmas_pos_ajuste_df(turmas_pos_reajuste_raspador.df)
    turmas_dicts = parsed_dataframe.to_dict('records')
    insert_items_RA_TURMAS(turmas_dicts)

# função privada dentro desse módulo
def _get_collection_SALAS_HORARIOS():
    try:
        return get_db.get_collection(DBCollections.TURMAS_SALAS_HORARIOS)
    except Exception as e:
        raise e
# função privada dentro desse módulo
def _get_collection_RA_TURMAS():
    try:
        return get_db.get_collection(DBCollections.RA_TURMAS)
    except Exception as e:
        raise e

def find_turmas_by_ra(ra : str, dia_semana=None,horario=None) -> list:
    try:
        response = list(_get_collection_RA_TURMAS().find({"RA":ra}))
        lista_disciplinas = []
        for item in response:
            disciplina = {}
            materia = list(_get_collection_SALAS_HORARIOS().find({'TURMA': str(item["TURMA"])}))[0]
            disciplina["Disciplina"] = materia["Disciplina"]
            disciplina["horário_pratica"] = materia["prática"]
            disciplina["horário_teoria"] = materia["teoria"]
            lista_disciplinas.append(disciplina)
        if dia_semana:
            if horario:
                lista_disciplinas = [ disciplina for disciplina in lista_disciplinas
                if (horario in str(disciplina["horário_pratica"])) and (dia_semana in str(disciplina["horário_pratica"]))
                or (horario in str(disciplina["horário_teoria"])) and dia_semana in str(disciplina["horário_teoria"])]
            else:
                lista_disciplinas = [ disciplina for disciplina in lista_disciplinas if dia_semana in str(disciplina["horário_pratica"]) or dia_semana in str(disciplina["horário_teoria"]) ]
        return lista_disciplinas
    except Exception as e:
        raise e
