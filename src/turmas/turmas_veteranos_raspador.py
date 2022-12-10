from requests import get
import pandas as pd
import unidecode

TURMAS_SALAS_HORARIOS_URL = "https://prograd.ufabc.edu.br/pdf/ajuste_2022_3_turmas.xlsx"
TURMAS_SALAS_HORARIOS = get(TURMAS_SALAS_HORARIOS_URL).content

with open("TURMAS_SALAS.xlsx","wb") as turmas:
    turmas.write(TURMAS_SALAS_HORARIOS)

df = pd.read_excel(TURMAS_SALAS_HORARIOS,sheet_name="AJUSTE_2022.3")

def clean_turmas_salas_horarios_df(df):
    # Realocando as colunas do Dataframe
    df.columns = df.iloc[0]
    df.drop(index=df.index[0], axis=0, inplace=True)
    # Limpeza dos elementos que são nulos
    for column in df.columns:
        df[column] = df[column].fillna(0)

    df.drop(['CURSO', 'Tipo de aula', 'TURMA',
       'turma', 'TEORIA', 'PRÁTICA',
       'CAMPUS', 'T-P-I', 'VAGAS TOTAIS',
       'VAGAS INGRESSANTES', 'VAGAS PARA VETERANOS',
       'TURMAS ALTA DEMANDA (não é possível soltar durante o ajuste)',
       'VAGAS TOTAIS', 'VAGAS RESERVADAS SISU',
       'VAGAS\nREMANESCENTES\n(PODEM OSCILAR DURANTE O AJUSTE)',
       'DOCENTE TEORIA 1', 'DOCENTE TEORIA 2', 'DOCENTE PRÁTICA 1',
       'DOCENTE PRÁTICA 2'],axis=1,inplace=True)
    df.columns = ['TURMA', 'Disciplina', 'Disciplina_del', 'teoria',
       'prática', 'TURNO']
    df["teoria"] = df["teoria"].apply(lambda x: x if type(x) is str else " ")
    df["prática"] = df["prática"].apply(lambda x: x if type(x) is str else " ")
    df.drop(['Disciplina_del'],axis=1,inplace=True)
    return df