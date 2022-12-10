def tratamento_ajuste(df):
    labels = df.loc[0].values.tolist()
    labels[5] = 'Codigo Disciplina'
    labels[6] = 'turma_cod'
    labels[20] = 'VAGAS REMANESCENTES'
    df.columns = labels
    df.drop([0],inplace=True)
    return df
