import requests # requisições http
import pandas as pd
from tabula import read_pdf
TURMAS_POS_REAJUSTE_URL = "https://prograd.ufabc.edu.br/pdf/reajuste_2022_3_matriculas_deferidas.pdf"
TURMAS_POS_REAJUSTE = requests.get(TURMAS_POS_REAJUSTE_URL).content

with open("turmas_pos_reajuste.pdf","wb") as turmas_pos_ajuste:
    turmas_pos_ajuste.write(TURMAS_POS_REAJUSTE)

df = read_pdf("turmas_pos_reajuste.pdf",pages="all",pandas_options={'header': None})

def clean_turmas_pos_ajuste_df(df):
    """
        Função que retorna a relação de turmas pos ajuste
    """
    # A Limpeza da Primeira página é especial e consiste em:

    # 1) limpeza das colunas extras
    df[0].drop(4,inplace=True,axis=1)

    # 2) limpeza das linhas extras
    df[0].drop([0],axis=0,inplace=True)

    # 3) renomear as colunas do dataframe inicial
    df[0] = df[0].rename(columns={0: "RA", 1: "TURMA",2:"DISCIPLINA",3:"TURMAS2",5:"CAMPUS"})

    # Todas as outras páginas seguem um padrão de limpeza que consiste em

    for idx, _ in enumerate(df):
        if idx >= 1:
            df[idx] = df[idx].rename(columns={0: "RA", 1: "TURMA",2:"DISCIPLINA",3:"TURMAS2",5:"CAMPUS"})
            df[idx].drop(4,inplace=True,axis=1)

    # Concatene todas as páginas pré-processadas num único dataframe
    df = pd.concat(df, axis=0, join="outer")

    df["TURNO"] = df["TURMAS2"].apply( lambda row : "Noturno" if "Noturno" in row else "Diurno" )
    # Limpe as colunas desnecessárias
    df.drop(["TURMAS2","TURNO","CAMPUS","DISCIPLINA"], axis=1,inplace=True)
    return df


