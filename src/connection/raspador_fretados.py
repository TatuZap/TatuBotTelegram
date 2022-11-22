import requests
import pandas as pd
BUS_URL = "https://pu.ufabc.edu.br/horarios-dos-onibus"
BUS_PAGE = requests.get(BUS_URL).content
tables_on_page = pd.read_html(BUS_PAGE)

# O Resultado desse método deve ser um dataframe único com 6 colunas:
#   - dias:            Pode ser de dois valores 'SEMANA' e 'SABADO'
#   - origem:          Pode ser de dois valores 'SA' e 'SBC'
#   - destino:         Pode ser de dois valores 'SA' e 'SBC'
#   - hora_partida:    Pode ser do valor de um horário, tipo '8:25' ou 'N/A' caso não tenha valor
#   - hora_chegada:    Pode ser do valor de um horário, tipo '8:25' ou 'N/A' caso não tenha valor
#   - linha:           O número da linha de onibus, pode ter valores de 1 a 6

def clean_bus_df(df):
    # Drop 'Somente desembarque Terminal Leste' 'Somente desembarque Terminal Leste.1' 'Terminal SBC'
    df[0] = df[0].drop("Somente desembarque Terminal Leste", axis='columns')
    df[0] = df[0].drop("Somente desembarque Terminal Leste.1", axis='columns')
    df[1] = df[1].drop("Terminal SBC", axis='columns')

    dataframe_zero_a = df[0][["Linha", "Santo André Partida", "São Bernardo Chegada"]]
    dataframe_zero_a = dataframe_zero_a.rename(columns={'Santo André Partida': 'hora_partida', 'São Bernardo Chegada': 'hora_chegada', 'Linha': 'linha'})
    dataframe_zero_a['origem'] = "SA"
    dataframe_zero_a['destino'] = "SBC"
    dataframe_zero_a['dias'] = "SEMANA"

    dataframe_zero_b = df[0][["Linha", "Partida", "Santo André Chegada"]]
    dataframe_zero_b = dataframe_zero_b.rename(columns={'Partida': 'hora_partida', 'Santo André Chegada': 'hora_chegada', 'Linha': 'linha'})
    dataframe_zero_b['origem'] = "SBC"
    dataframe_zero_b['destino'] = "SA"
    dataframe_zero_b['dias'] = "SEMANA"

    dataframe_one = df[1]
    dataframe_one = dataframe_one.rename(columns={'Campus SBC Partida': 'hora_partida', 'Campus SBC Chegada': 'hora_chegada', 'Linha': 'linha'})
    dataframe_one['origem'] = "SBC"
    dataframe_one['destino'] = "SBC"
    dataframe_one['dias'] = "SEMANA"

    dataframe_two_a = df[2][["Linha", "Santo André Partida", "São Bernardo Chegada"]]
    dataframe_two_a = dataframe_two_a.rename(columns={'Santo André Partida': 'hora_partida', 'São Bernardo Chegada': 'hora_chegada', 'Linha': 'linha'})
    dataframe_two_a['origem'] = "SA"
    dataframe_two_a['destino'] = "SBC"
    dataframe_two_a['dias'] = "SABADO"

    dataframe_two_b = df[2][["Linha", "Santo André Partida", "São Bernardo Chegada"]]
    dataframe_two_b = dataframe_two_a.rename(columns={'Santo André Partida': 'hora_partida', 'São Bernardo Chegada': 'hora_chegada', 'Linha': 'linha'})
    dataframe_two_b['origem'] = "SBC"
    dataframe_two_b['destino'] = "SA"
    dataframe_two_b['dias'] = "SABADO"

    parsed_dataframe = pd.concat([
        dataframe_zero_a,
        dataframe_zero_b,
        dataframe_one,
        dataframe_two_a,
        dataframe_two_b,
    ])

    for column in parsed_dataframe.columns:
        parsed_dataframe.loc[(parsed_dataframe[column] == "---"),column] = 'N/A'

    # for column in parsed_dataframe.columns:
    # if column == "hora_partida" or column == "hora_chegada":
    #     parsed_dataframe[column] = parsed_dataframe[column].apply( lambda x : datetime.datetime(2022,1,1,int(x.split(":")[0]),int(x.split(":")[1])).isoformat() if x != "---" else "N/A")
    #     parsed_dataframe.loc[(parsed_dataframe[column] == "---"),column] = 'N/A'


    return parsed_dataframe
