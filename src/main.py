from load.DB import get_db,DBCollections

turmas_por_ra_collection = get_db[DBCollections.TURMAS_POR_RA]

def turmas(RA):
    QUERY = {"RA": str(RA)}
    result = list(turmas_por_ra_collection.find(QUERY))
    lista = result[0]["TURMAS"]
    for res in lista:del res['_id']
    lista_clean = [dict(item) for item in {tuple(dict.items()) for dict in lista}]
    for disciplina in lista_clean:
        teoria = disciplina['HORÁRIO TEORIA']
        pratica = disciplina['HORÁRIO PRÁTICA']
        nome = disciplina['DISCIPLINA - TURMA']

        if teoria == 0:
            print('Disciplina: {}, Horário Prática: {}'.format(nome,pratica)) 
        if pratica == 0:
            print('Disciplina: {}, Horário Teoria: {}'.format(nome,teoria)) 
    return lista_clean

print('Digite seu RA:')
RA = input()
turmas(RA)