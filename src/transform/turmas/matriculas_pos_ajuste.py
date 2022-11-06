import pandas as pd
import unidecode

def tratamento_matriculas_pos_ajuste(df):
    df.rename(columns={df.columns[0]: 'new'},inplace=True)
    df['new'] = df['new'].str.strip()
    df[['RA', 'CODIGO_TURMA', 'REMOVER','REMOVER','TURMA']] = df['new'].str.split(" ",4, expand=True)

    df1 = df.loc[df['RA'].str.len() == 11]
    df2 = df.loc[df['RA'].str.len() > 11]
    
    def spliter(item):return unidecode.unidecode(item)
    data = df2["RA"].apply(spliter).str.split(" ",4, expand=True).values.tolist()
    df3 = pd.DataFrame(data,columns =['RA', 'CODIGO_TURMA', 'REMOVER','REMOVER','TURMA'] )
        #df2[['RA', 'CODIGO_TURMA', 'REMOVER','REMOVER','TURMA']] = df2.loc[:,"RA"].apply(spliter).str.split(" ",4, expand=True)
    df = pd.concat([df1,df2])
    df.drop(columns=['new', 'REMOVER'],inplace=True)
    df['TURMA'] = df['TURMA'].str.strip()
    return df
