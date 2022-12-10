import requests # requisições http
import pandas as pd 
import tabula

from tabula import read_pdf

CALENDARIO_URL = "https://prograd.ufabc.edu.br/pdf/calendario_academico_administrativo_2022.pdf"
CALENDARIO = requests.get(CALENDARIO_URL).content

with open("calendario.pdf","wb") as calendario:
    calendario.write(CALENDARIO)

tables_on_page = read_pdf("calendario.pdf",pages="all",lattice=True, guess=False,pandas_options={'header': None})

