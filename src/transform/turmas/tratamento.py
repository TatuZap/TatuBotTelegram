from .matriculas_pos_ajuste import tratamento_matriculas_pos_ajuste as tratamento_matriculas_pos_ajuste
from .turmas_ingressantes import tratamento_turmas_ingressantes as tratamento_turmas_ingressantes
from .ajuste import tratamento_ajuste as tratamento_ajuste
import json
import os

def list_df_to_json(dfs):
    list = []
    for data in dfs:
        df = data["df"]
        list.append(json.loads(df.to_json(orient="table",index=False))['data'])
    return list
current_path = os.path.dirname(os.path.abspath(__file__))
sep = '\\' if os.name == 'nt' else '/'
def to_json_file(dfs):
    i=0
    for data in dfs:
        df = data["df"]
        i = i + 1
        df.to_json(current_path + sep + 'output' + sep + data["file_name"]+'.json',orient="table",index=False)
    return list


def tratamento_json(get_all_dataframes):
    dfs = get_all_dataframes()
    dfs[0]["df"]= tratamento_ajuste(dfs[0]["df"])
    dfs[1]["df"]= tratamento_matriculas_pos_ajuste(dfs[1]["df"])
    dfs[3]["df"] = tratamento_turmas_ingressantes(dfs[3]["df"])
    return list_df_to_json(dfs)

def tratamento_df(get_all_dataframes):
    dfs = get_all_dataframes()
    dfs[0]["df"] = tratamento_ajuste(dfs[0]["df"])
    dfs[1]["df"] = tratamento_matriculas_pos_ajuste(dfs[1]["df"])
    dfs[3]["df"]= tratamento_turmas_ingressantes(dfs[3]["df"])
    return dfs


