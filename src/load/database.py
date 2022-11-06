import os
from dataclasses import dataclass
from pymongo import MongoClient

from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), '.env')) # carrega as variáveis do arquivo .env local 
@dataclass
class DBCollections:
    TURMAS = "turmas"
    FRETADOS = "fretados"
    CATALOGO = "catalogo"
    AJUSTE = "matriculas_deferidas_pos_ajuste_2022.3.xlsx.json"
    REAJUSTE = "reajuste_2022_3_matriculas_deferidas.xlsx.json"
    DISCIPLINAS = "TURMAS_VETERANOS_2022.3.xlsx.json"
    TURMAS_POR_RA = "turmas_por_ra"
@dataclass
class DBconfig:
    DB_URL = "mongodb+srv://{}:{}@cluster0.dw7svve.mongodb.net/?retryWrites=true&w=majority".format(os.getenv("MONGO_USER_NAME"),os.getenv("MONGO_SECRET"))
    DB_NAME = "tatuzap"
    DB_COLLECTIONS = DBCollections


"""
   Singleton pattern by module
"""
get_db = MongoClient(DBconfig.DB_URL)[DBconfig.DB_NAME]
