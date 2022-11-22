import requests
import unidecode
import nltk
import pandas as pd
import numpy as np
from nltk.corpus import stopwords

STOPWORDS = stopwords.words('portuguese')
CATALOGO_URL = "https://prograd.ufabc.edu.br/pdf/catalogo_disciplinas_graduacao_2021_2022_0722.xlsx"
CATALOGO_XLSX  = requests.get(CATALOGO_URL).content
catalogo_df = pd.read_excel(CATALOGO_XLSX)

def clean_catalogo_df(df):
    df = df.rename(columns={'SIGLA': 'sigla', 'DISCIPLINA': 'disciplina', 'RECOMENDAÇÃO': 'recomendacoes', "OBJETIVOS":"objetivos","EMENTA":"ementa","BIBLIOGRAFIA BÁSICA":"BB","BIBLIOGRAFIA COMPLEMENTAR":"BC"})
    df = df.replace(np.nan,"")
    df["apelido"] = df["disciplina"].apply(lambda x: "".join([ w[0] for w in x.lower().split() if w not in STOPWORDS]))
    df["disciplina"] = df["disciplina"].apply(lambda x: unidecode.unidecode(x))
    return df