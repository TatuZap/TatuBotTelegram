def tratamento_turmas_ingressantes(df):
    def add_space(item): 
        if len(str(item))<12 : return str(item) + '  '
        return str(item)
    df.iloc[:,0] = df.iloc[:,0].apply(add_space)
    df['temp'] = df.iloc[:,0].astype(str) + df.iloc[:,1].astype(str) + df.iloc[:,2].astype(str)
    df['temp'] = df['temp'].str.replace('nan','')
    df.drop(df.columns[[0,1,2]],axis=1,inplace=True)
    df[['RA','CURSO']] = df.iloc[:,6].str.split(" ",1,expand=True)
    df.drop(df.columns[[6]],axis=1,inplace=True)
    df['temp'] = df.iloc[:,3].astype(str) + df.iloc[:,4].astype(str)
    df['temp'] = df['temp'].str.replace('nan','')
    df.drop(df.columns[[3,4]],axis=1,inplace=True)
    df.rename(columns={"temp": "TURNO"},inplace=True)
    return df
