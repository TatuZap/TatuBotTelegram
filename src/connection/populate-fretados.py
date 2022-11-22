import fretados_model
import catalogo_model
import usuario_model
import datetime
# Como popular o banco de dados
fretados_model.populate_database()

# ##catalogo_model.populate_database()

for item in usuario_model.list_all():
    print(item)

# # Listando tudo que foi recuperado
# print("Listando todos os Fretados")
# for item in fretados_model.list_all():
#     print(item)

tempo_limite = "24:00"

#print(fretados_model.next_bus("SA","SBC",tempo))
for item in fretados_model.next_bus("SA","SBC",tempo,tempo_limite,5):
    print(item)

# print("Listando todos as turmas do catálogo")
# for item in catalogo_model.list_all():
#     print(item)


# Listando os que saem de SA e vão para SBC
# for item in fretados_model.next_bus("SA", "SBC", ""):
#     print(item)

# #### listando os que saem de SBC e vão para SA ####
# for item in fretados_model.next_bus("SA", "SBC", ""):
#     print(item)

#### listando os que saem de SBC e vão para SBC ####
# for item in fretados_model.next_bus("SBC", "SBC", ""):
#     print(item)

# #### listando o primeiro fretado que achar que é da linha 2 ####
# print(fretados_model.find_by_linha(2))
