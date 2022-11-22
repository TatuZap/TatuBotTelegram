import requests # requisições http
import pandas as pd 
RESTAURANT_URL = "https://proap.ufabc.edu.br/nutricao-e-restaurantes-universitarios/cardapio-semanal"
RESTAURANT_PAGE = requests.get(RESTAURANT_URL).content
tables_on_page = pd.read_html(RESTAURANT_PAGE)[0] # ja devolve a tabela correta

def clean_restaurant_df(df):
    """
        Função que retorna o cardapio do RU da ufabc
    """
    # seleciona a tabela que foi raspada do site da ufabc
    df = df.drop(1, axis='columns') # dropa o campo de informações 
    df_dias = df.iloc[[ x for x in range(0,df.shape[0],2)]]
    df_comida = df.iloc[[ x for x in range(1,df.shape[0],2)]] 
    df_dias = df_dias.rename(columns={0:"data"}) # renomeia a coluna dos dias
    df_comida = df_comida.rename(columns={0:"informacoes"}) # renomeia a coluna da comida 
    df_comida["informacoes"] = df_comida["informacoes"].apply( lambda str : str.lower() )
    df_dias[['data','dia_semana']] = df_dias["data"].str.split(" • ",expand=True,) 
    df_dias["dia_semana"] = df_dias["dia_semana"].apply( lambda string_day: list(filter(lambda x : x[1] == string_day, list(enumerate(["Seg","Ter","Qua","Qui","Sex","Sáb"]))))[0][0])
    df_comida[['almoço','jantar',"saladas","sobremesas"]] = df_comida["informacoes"].str.split(r"\b(almoço|jantar|saladas|sobremesas)\b",expand=True,)[[2,4,6,8]]
    df_comida.drop("informacoes",inplace=True, axis=1)
    df_dias = df_dias.reset_index(drop=True)
    df_comida = df_comida.reset_index(drop=True) 
    df = pd.concat([df_dias, df_comida], axis=1,join="inner") 
    return df
