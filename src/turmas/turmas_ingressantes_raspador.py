from requests import get
import pandas as pd
from tabula import read_pdf
TURMAS_INGRESSANTES_URL = "https://prograd.ufabc.edu.br/pdf/turmas_ingressantes_2022_3.pdf"
TURMAS_INGRESSANTES = get(TURMAS_INGRESSANTES_URL).content

with open("turmas_ingressantes.pdf","wb") as turmas:
    turmas.write(TURMAS_INGRESSANTES)

df = read_pdf("turmas_ingressantes.pdf",stream=True,guess=False,pages='all', pandas_options={'header': None})


def clean_turmas_ingressantes_df(df):
    df[0].columns = df[0].iloc[1]
    df[0].drop([0,1], axis=0, inplace=True)
    df[0].drop(index=df[0].index[-1],axis=0,inplace=True)

    for idx, _ in enumerate(df):
        if idx > 0:
            df[idx].columns = df[0].columns
            df[idx].drop([0], axis=0, inplace=True)
            df[idx].drop(index=df[idx].index[-1],axis=0,inplace=True)
            df[idx].drop(['CURSO'], axis=1,inplace=True)
            df[idx]["RA"] = df[idx]["RA"].apply(lambda x: int(x) if type(x) is float else int(x[:11]))
    df[0].drop(['CURSO'], axis=1,inplace=True)
    df = pd.concat(df, axis=0, join="outer")
    df.drop(["TURMA2","TURNO","CAMPUS","DISCIPLINA"], axis=1,inplace=True)
    return df