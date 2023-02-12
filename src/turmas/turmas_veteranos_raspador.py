from requests import get
import pandas as pd
import unidecode

# TURMAS_SALAS_HORARIOS_URL = "https://prograd.ufabc.edu.br/pdf/ajuste_2022_3_turmas.xlsx"
TURMAS_SALAS_HORARIOS_URL = "https://prograd.ufabc.edu.br/pdf/turmas_salas_docentes_2023_1.xlsb"
TURMAS_SALAS_HORARIOS = get(TURMAS_SALAS_HORARIOS_URL).content

with open("TURMAS_SALAS.xlsx","wb") as turmas:
    turmas.write(TURMAS_SALAS_HORARIOS)

# df = pd.read_excel(TURMAS_SALAS_HORARIOS,sheet_name="AJUSTE_2022.3")
xls = pd.ExcelFile(TURMAS_SALAS_HORARIOS)
df = pd.read_excel(xls)


def clean_turmas_salas_horarios_df(df):
    # Removendo as linhas sem uso
    df.drop(labels=range(0, 53), axis=0, inplace=True)
    # Realocando as colunas do Dataframe
    df.columns = df.iloc[0]
    df.drop(index=df.index[0], axis=0, inplace=True)
    # Limpeza dos elementos que são nulos
    for column in df.columns:
        df[column] = df[column].fillna(0)

    df.drop(['CURSO', 'Disciplina',
       'turma', 'TEORIA', 'PRÁTICA',
       'CAMPUS', 'T-P-I', 'VAGAS TOTAIS',
       'VAGAS INGRESSANTES', 'VAGAS REMANESCENTES',
       'DOCENTE TEORIA', 'DOCENTE TEORIA 2', 'DOCENTE PRÁTICA',
       'DOCENTE PRÁTICA 2'],axis=1,inplace=True)
    df.columns = ['TURMA', 'Disciplina', 'teoria',
       'prática', 'TURNO']
    df["teoria"] = df["teoria"].apply(lambda x: x if type(x) is str else " ")
    df["prática"] = df["prática"].apply(lambda x: x if type(x) is str else " ")
    return df