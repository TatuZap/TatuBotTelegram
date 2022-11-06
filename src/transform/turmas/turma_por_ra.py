import json
import os
def get_all_ra(ajuste,reajuste):
    all_ra = reajuste.distinct("RA") + ajuste.distinct("RA")
    return list(set(all_ra))

def tratamento_matriculas_pos_ajuste_pos_carga(ajuste):
    aluno_bug = ajuste.find({"CODIGO_TURMA":None})
    error = list(aluno_bug)
    for error_ in error:
        aluno_bug = ajuste.find({"RA":error_["RA"]})
        split_data = error_["RA"].split("\xa0",3)
        aluno_fix = {"$set": {
                                "RA": split_data[0],
                                "CODIGO_TURMA": split_data[1],
                                "TURMA":split_data[-1].replace("\xa0"," "),
                            }
                    }
        print(aluno_fix)
        ajuste.update_one({"RA": error_["RA"]},aluno_fix)

def tratamento_turma_por_ra(ajuste,reajuste,turmas,RA):
    QUERY_AJUSTE = {"RA":RA}
    QUERY_REAJUSTE = {"RA":int(RA)}
    disciplinas_ajuste = ajuste.find(QUERY_AJUSTE)
    disciplinas_reajuste = reajuste.find(QUERY_REAJUSTE)

    disciplinas = list(disciplinas_ajuste) + list(disciplinas_reajuste)

    disciplinas = [disciplinas]
    turmas_por_RA = []
    for discente in disciplinas:
        aluno = {
            "RA": str(discente[0]["RA"]),
            "TURMAS" : []
        }

        for disciplina in discente:
            try:
                CODIGO_TURMA = disciplina['CODIGO_TURMA']
            except:
                CODIGO_TURMA = disciplina['TURMA']
            QUERY_TURMAS = {"CÓDIGO":CODIGO_TURMA}
            turma_por_codigo = turmas.find(QUERY_TURMAS)
            for turma in turma_por_codigo:
                aluno["TURMAS"].append(turma)

        turmas_por_RA.append(aluno)
    return turmas_por_RA
sep = '\\' if os.name == 'nt' else '/'
def save_json(data):
    path=os.path.realpath('./src/transform/turmas') + sep + "turma_por_ra.json"
    jsonString = json.dumps(data,default=str)
    jsonFile = open(path, "w")
    jsonFile.write(jsonString)
    jsonFile.close()

def turmas_por_ra(all_ra,ajuste,reajuste,turmas):
    data = []
    #print(tratamento_turma_por_ra(ajuste,reajuste,turmas,all_ra[15]))
    index = 0
    for RA in all_ra:
        index = index + 1
        print(str(index)+ " / " + str(len(all_ra)))
        data.append(tratamento_turma_por_ra(ajuste,reajuste,turmas,str(RA))[0])
    save_json(data)
    return data

def tratamento_ra_pos_carga(ajuste):
    aluno_bug = ajuste.find({"CODIGO_TURMA":None})
    error = list(aluno_bug)
    for error_ in error:
        aluno_bug = ajuste.find({"RA":error_["RA"]})
        split_data = error_["RA"].split("\xa0",3)
        aluno_fix = {"$set": {
                                "RA": split_data[0],
                                "CODIGO_TURMA": split_data[1],
                                "TURMA":split_data[-1].replace("\xa0"," "),
                            }
                    }
        print(aluno_fix)
        ajuste.update_one({"RA": error_["RA"]},aluno_fix)

