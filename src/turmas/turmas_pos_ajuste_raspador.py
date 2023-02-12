import requests # requisições http
import pandas as pd
from tabula import read_pdf
#TURMAS_POS_AJUSTE_URL = "https://prograd.ufabc.edu.br/pdf/matriculas_deferidas_pos_ajuste_2022.3.pdf"
TURMAS_POS_AJUSTE_URL = "https://prograd.ufabc.edu.br/pdf/ajuste_2023_1_deferidos_pos_ajuste.pdf"
TURMAS_POS_AJUSTE = requests.get(TURMAS_POS_AJUSTE_URL).content

with open("turmas_pos_ajuste.pdf","wb") as turmas_pos_ajuste:
    turmas_pos_ajuste.write(TURMAS_POS_AJUSTE)

df = read_pdf("turmas_pos_ajuste.pdf",pages="all",stream=True, guess=False,pandas_options={'header': None})

def clean_turmas_pos_ajuste_df(df):
    """
        Função que retorna a relação de turmas pos ajuste
    """

 # Todas as outras páginas seguem um padrão de limpeza que consiste em

    for idx, _ in enumerate(df):
        # A Limpeza da Primeira página é especial e consiste em:

        # 1) limpeza das colunas extras, quando existem
        if 3 in df[idx].columns:
            df[idx].drop(3,inplace=True,axis=1)

        # 2) limpeza das linhas extras
        df[idx].drop([0],axis=0,inplace=True)
        df[idx].drop([1],axis=0,inplace=True)
        df[idx].drop(index=df[idx].index[-1],axis=0,inplace=True)

        # 3) renomear as colunas do dataframe inicial
        df[idx] = df[idx].rename(columns={0: "RA", 1:"TURMA", 2: "TURMAS2"})

    # Concatene todas as páginas pré-processadas num único dataframe
    df = pd.concat(df, axis=0, join="outer")
    df.drop("TURMAS2",inplace=True,axis=1)
    df.columns = ["RA","TURMA"]
    #df = df.rename(columns={"TURMAS": "COD", "TURMAS2":"TURMA"})
    return df