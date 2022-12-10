import requests # requisições http
import pandas as pd
from tabula import read_pdf
TURMAS_POS_AJUSTE_URL = "https://prograd.ufabc.edu.br/pdf/matriculas_deferidas_pos_ajuste_2022.3.pdf"
TURMAS_POS_AJUSTE = requests.get(TURMAS_POS_AJUSTE_URL).content

with open("turmas_pos_ajuste.pdf","wb") as turmas_pos_ajuste:
    turmas_pos_ajuste.write(TURMAS_POS_AJUSTE)

df = read_pdf("turmas_pos_ajuste.pdf",pages="all",stream=True, guess=False,pandas_options={'header': None})

def clean_turmas_pos_ajuste_df(df):
    """
        Função que retorna a relação de turmas pos ajuste
    """

    # A Limpeza da Primeira página é especial e consiste em:

    # 1) limpeza das colunas extras
    df[0].drop(1,inplace=True,axis=1)
    df[0].drop(3,inplace=True,axis=1)

    # 2) limpeza das linhas extras
    df[0].drop([0],axis=0,inplace=True)
    df[0].drop([1],axis=0,inplace=True)
    df[0].drop(index=df[0].index[-1],axis=0,inplace=True)

    # 3) renomear as colunas do dataframe inicial
    df[0] = df[0].rename(columns={0: "RA TURMAS", 2: "TURMAS2"})

    # Todas as outras páginas seguem um padrão de limpeza que consiste em

    for idx, _ in enumerate(df):
        if idx >= 1:
            # 1) renomear as colunas do dataframe 
            df[idx] = df[idx].rename(columns={0: "RA TURMAS", 1: "TURMAS2"})
            # 2) Limpeza das possiveis colunas extras
            if 2 in df[idx].columns:
                df[idx].drop(2,inplace=True,axis=1)
            # 3) Limpeza das linhas extras
            df[idx].drop([0],axis=0,inplace=True)
            df[idx].drop(index=df[idx].index[-1],axis=0,inplace=True)

    # Concatene todas as páginas pré-processadas num único dataframe
    df = pd.concat(df, axis=0, join="outer")

    # Separe os dados RA e TURMAS que estavam juntos
    df[["RA","TURMAS"]] = df["RA TURMAS"].str.split(" ",expand=True)
    # Limpe as colunas desnecessárias
    df.drop("RA TURMAS",inplace=True,axis=1)
    df.drop("TURMAS2",inplace=True,axis=1)
    df.columns = ["RA","TURMA"]
    #df = df.rename(columns={"TURMAS": "COD", "TURMAS2":"TURMA"})
    return df