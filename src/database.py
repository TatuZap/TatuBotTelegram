import os
from dataclasses import dataclass
from pymongo import MongoClient


from dotenv import load_dotenv
load_dotenv(os.path.join(os.getcwd(), '.env')) # carrega as variáveis do arquivo .env local ]
@dataclass
class DBCollections:
    RA_TURMAS = "ra_turmas"
    TURMAS_SALAS_HORARIOS = "turmas_salas_horarios"
    FRETADOS = "fretados"
    CATALOGO = "catalogo"
    USUARIO =  "usuario"
    RESTAURANTE = "restaurante"
@dataclass
class DBconfig:
    DB_URL = "mongodb+srv://{}:{}@cluster0.dw7svve.mongodb.net/?retryWrites=true&w=majority".format(os.getenv("MONGO_USER_NAME"),os.getenv("MONGO_SECRET"))
    DB_NAME = "tatuzap"
    DB_COLLECTIONS = DBCollections

"""
   Singleton pattern by module
"""
get_db = MongoClient(DBconfig.DB_URL)[DBconfig.DB_NAME]
