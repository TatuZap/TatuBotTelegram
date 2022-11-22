from transform.turmas.tratamento import tratamento_json,tratamento_df, to_json_file
from transform.turmas.turma_por_ra import tratamento_turma_por_ra,get_all_ra,turmas_por_ra,tratamento_matriculas_pos_ajuste_pos_carga
from extract.turmas.get_files import file_output
from extract.turmas.extrator import get_all_dataframes
from load.DB import get_db,DBCollections
from load.turmas.carga import load_one,load_json
import os
import json

#Retorna todos os dados das turmas em json
#tratamento_json(get_all_dataframes)

#retorna todos os dados das turmas em dataframes
#dfs = tratamento_df(get_all_dataframes)
#Cria arquivos json na pasta output
#to_json_file(dfs)

# Get Collections
ajuste = get_db[DBCollections.AJUSTE]
reajuste = get_db[DBCollections.REAJUSTE]
turmas = get_db[DBCollections.DISCIPLINAS]

#Carga
#load_json(get_db,file_output)

#RA = "11202020902"
#Retorna todas as informações de turmas por RA
#turma_por_ra = tratamento_turma_por_ra(ajuste,reajuste,turmas,RA)
#print(turma_por_ra)

#tratamento_matriculas_pos_ajuste_pos_carga(ajuste)

#Gera JSON de dados consolidados das turmas por RA
#data = turmas_por_ra(get_all_ra(ajuste,reajuste),ajuste,reajuste,turmas)

#Sobe dados consolidados das turmas por RA para o banco
sep = '\\' if os.name == 'nt' else '/'
path = os.path.realpath('./src/transform/turmas')+sep+"turma_por_ra.json" 
load_one(get_db,path,"turmas_por_ra")

#Lista todos os RA
#print(get_all_ra(ajuste,reajuste))