import requests
import pandas as pd

BUS_URL = "https://pu.ufabc.edu.br/horarios-dos-onibus"
BUS_PAGE = requests.get(BUS_URL).content
tables_on_page = pd.read_html(BUS_PAGE)

# O Resultado desse método deve ser um dataframe único com 6 colunas:
#   - dias:                       Pode ser de dois valores 'SEMANA' e 'SABADO'
#   - origem:                     Pode ser dos valores: 'SA' ou 'SBC' ou 'TERMINAL-SBC' (Obs.: não pode ser terminal leste pois é apenas desembarque, temos um campo especifico para isso)
#   - destino:                    Pode ser dos valores: 'SA' ou 'SBC' ou 'TERMINAL-SBC' (Obs.: não pode ser terminal leste pois é apenas desembarque, temos um campo especifico para isso)
#   - hora_partida:               Pode ser do valor de um horário, tipo '8:25' ou 'N/A' caso não tenha valor
#   - hora_chegada:               Pode ser do valor de um horário, tipo '8:25' ou 'N/A' caso não tenha valor
#   - desembarque_terminal_leste: Caso tenha desembarque no Terminal Leste é o valor de um horário, tipo '8:25', caso contrário, 'N/A'
#   - linha:                      O número da linha de onibus, pode ter valores de 1 a 6

def clean_bus_df(df):
    # Pega os fretados do dataframe[0] que vao de SA a SBC
    dataframe_zero_a = df[0][["Linha", "Santo André Partida", "Somente desembarque Terminal Leste", "São Bernardo Chegada"]]
    dataframe_zero_a = dataframe_zero_a.rename(columns={
        'Santo André Partida': 'hora_partida',
        'Somente desembarque Terminal Leste': 'desembarque_terminal_leste',
        'São Bernardo Chegada': 'hora_chegada',
        'Linha': 'linha',
    })
    dataframe_zero_a['origem'] = "SA"
    dataframe_zero_a['destino'] = "SBC"
    dataframe_zero_a['dias'] = "SEMANA"

    # Pega os fretados do dataframe[0] que vao de SBC a SA
    dataframe_zero_b = df[0][["Linha", "Partida", "Somente desembarque Terminal Leste.1", "Santo André Chegada"]]
    dataframe_zero_b = dataframe_zero_b.rename(columns={
        'Partida': 'hora_partida',
        'Somente desembarque Terminal Leste.1': 'desembarque_terminal_leste',
        'Santo André Chegada': 'hora_chegada',
        'Linha': 'linha',
    })
    dataframe_zero_b['origem'] = "SBC"
    dataframe_zero_b['destino'] = "SA"
    dataframe_zero_b['dias'] = "SEMANA"

    # Pega os fretados do dataframe[1] que vao de SBC a TERMINAL-SBC
    dataframe_one_a = df[1][["Linha", "Campus SBC Partida", "Terminal SBC"]]
    dataframe_one_a = dataframe_one_a.rename(columns={
        'Campus SBC Partida': 'hora_partida',
        'Terminal SBC': 'hora_chegada',
        'Linha': 'linha'
    })
    dataframe_one_a['origem'] = "SBC"
    dataframe_one_a['destino'] = "TERMINAL-SBC"
    dataframe_one_a['dias'] = "SEMANA"
    dataframe_one_a['desembarque_terminal_leste'] = "N/A"

    # Pega os fretados do dataframe[1] que vao de TERMINAL-SBC a SBC
    dataframe_one_b = df[1][["Linha", "Terminal SBC", "Campus SBC Chegada"]]
    dataframe_one_b = dataframe_one_b.rename(columns={
        'Terminal SBC': 'hora_partida',
        'Campus SBC Chegada': 'hora_chegada',
        'Linha': 'linha'
    })
    dataframe_one_b['origem'] = "TERMINAL-SBC"
    dataframe_one_b['destino'] = "SBC"
    dataframe_one_b['dias'] = "SEMANA"
    dataframe_one_b['desembarque_terminal_leste'] = "N/A"

    # Pega os fretados do dataframe[2] que vao de SA a SBC
    dataframe_two_a = df[2][["Linha", "Santo André Partida", "São Bernardo Chegada"]]
    dataframe_two_a = dataframe_two_a.rename(columns={'Santo André Partida': 'hora_partida', 'São Bernardo Chegada': 'hora_chegada', 'Linha': 'linha'})
    dataframe_two_a['origem'] = "SA"
    dataframe_two_a['destino'] = "SBC"
    dataframe_two_a['dias'] = "SABADO"
    dataframe_two_a['desembarque_terminal_leste'] = "N/A"

    # Pega os fretados do dataframe[2] que vao de SBC a SA
    dataframe_two_b = df[2][["Linha", "Partida", "Santo André Chegada"]]
    dataframe_two_b = dataframe_two_b.rename(columns={'Partida': 'hora_partida', 'Santo André Chegada': 'hora_chegada', 'Linha': 'linha'})
    dataframe_two_b['origem'] = "SBC"
    dataframe_two_b['destino'] = "SA"
    dataframe_two_b['dias'] = "SABADO"
    dataframe_two_b['desembarque_terminal_leste'] = "N/A"

    # Concatena os dataframes resultantes
    parsed_dataframe = pd.concat([
        dataframe_zero_a,
        dataframe_zero_b,
        dataframe_one_a,
        dataframe_one_b,
        dataframe_two_a,
        dataframe_two_b,
    ])

    # Substitui todos os valores '---' por 'N/A'
    for column in parsed_dataframe.columns:
        parsed_dataframe.loc[(parsed_dataframe[column] == "---"),column] = 'N/A'

    # Limpa o dataframe de linhas com hora_chegada ou hora_partida sem informação
    parsed_dataframe = parsed_dataframe[parsed_dataframe.hora_chegada != 'N/A']
    parsed_dataframe = parsed_dataframe[parsed_dataframe.hora_partida != 'N/A']

    return parsed_dataframe
