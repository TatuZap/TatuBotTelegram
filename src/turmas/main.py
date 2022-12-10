from load.DB import get_db,DBCollections

# tratamento()

turmas_por_ra_collection = get_db[DBCollections.TURMAS_POR_RA]

def turmas(RA):
    QUERY = {"RA": str(RA)}
    result = list(turmas_por_ra_collection.find(QUERY))
    lista = result[0]["TURMAS"]
    for res in lista:del res['_id']
    lista_clean = [dict(item) for item in {tuple(dict.items()) for dict in lista}]
    for disciplina in lista_clean:print(disciplina)
    return lista_clean

print('Digite seu RA:')
RA = input()
turmas(RA)
