import unittest
import fretados_model
import json 


class TestFretadoModel(unittest.TestCase):
    """
        Todos os casos de testes devem ser escritos como funções
        que começam com test.
    """
    def test_list_all_len(self):
        """
            O list_all após população deve retornar ao menos 1 elemento
        """
        #fretados_model.populate_database() # garante que o database foi populado
        all_bus = fretados_model.list_all() # lista todos
        self.assertGreater(len(list(all_bus)), 0,"A lista deve ser não nula")

    def test_insert_item_inserts(self):
        """
            A função de inserção de um único elemento não deve retornar erros.
        """
        bus = {
            "linha": -1,
            "hora_partida": "07:07",
            "hora_chegada": "07:07",
            "origem":"test_insert_item_inserts",
            "destino":"test_insert_item_inserts",
            "dias":"SEMANA"
        }
        try:
            fretados_model.insert_item(json.loads(json.dumps(bus)))
        except Exception as e:
            self.fail("A inserção não deve retornar Erro")
    
    def test_insert_item_find(self):
        """
            Um elemento inserido deve ser recuperável sem retornar erros.
        """
        bus = {
            "linha": -1,
            "hora_partida": "07:07",
            "hora_chegada": "07:07",
            "origem":"test_insert_item_find",
            "destino":"test_insert_item_find",
            "dias":"SEMANA"
        }
        try:
            fretados_model.insert_item(json.loads(json.dumps(bus)))
            fretados_model.find_by_all_fields(
                linha=bus["linha"],
                hora_partida=bus["hora_partida"],
                hora_chegada=bus["hora_chegada"],
                origem=bus["origem"],
                destino=bus["destino"],
                dia_semana=bus["dias"]                
            )
            #self.assertGreater(len(list(response_find)), 0, "Ao inserir um elemento, este deve estar no banco.")
        except Exception as e:
            self.fail("Um elemento inserido deve ser recuperado sem erro")


    def test_insert_item_find_retrieve(self):
        """
            Um elemento inserido deve ser recuperado.
        """
        bus = {
            "linha": -1,
            "hora_partida": "07:07",
            "hora_chegada": "07:07",
            "origem":"test_insert_item_find_retrieve",
            "destino":"test_insert_item_find_retrieve",
            "dias":"SEMANA"
        }

        fretados_model.insert_item(json.loads(json.dumps(bus)))
        response = fretados_model.find_by_all_fields(
            linha=bus["linha"],
            hora_partida=bus["hora_partida"],
            hora_chegada=bus["hora_chegada"],
            origem=bus["origem"],
            destino=bus["destino"],
            dia_semana=bus["dias"]                
        )
        bus_retrieved = list(response)[0]
        del bus_retrieved["_id"] # deleta o atributo "_id" que vem do banco de dados e não usamos para nada
        self.assertEqual(sorted(json.loads(json.dumps(bus)).items()), sorted(json.loads(json.dumps(bus_retrieved)).items()), "O elemento inserido deve ser igual ao recuperado")

    def test_insert_items_inserts(self):
        """
            A função de inserção de multiplos elementos não deve retornar erros.
        """
        bus_1 = {
            "linha": -1,
            "hora_partida": "07:07",
            "hora_chegada": "07:07",
            "origem":"test_insert_items_inserts",
            "destino":"test_insert_items_inserts",
            "dias":"SEMANA"
        }
        bus_2 = {
            "linha": 0,
            "hora_partida": "07:07",
            "hora_chegada": "07:07",
            "origem":"test_insert_items_inserts",
            "destino":"test_insert_items_inserts",
            "dias":"SABADO"
        }
        bus = [ json.loads(json.dumps(bus)) for bus in [bus_1,bus_2]]
        try:
            response = fretados_model.insert_items(bus)
        except Exception as e:
            self.fail("A inserção de multiplos elementos não deve retornar Erro")

    def test_find_by_linha_len(self):
        """
            Ao buscar um fretado de uma determinada linha
            num determinado dia da semana, devemos obter
            uma lista de fretados.
        """
        fretados_model.populate_database() # garante que o database foi populado
        day = 0 # indice da segunda-feira
        line = 1

        response = fretados_model.find_by_linha(line,day)

        self.assertGreater(len(list(response)), 0, "A lista de fretatos recuperados para uma linha valida deve ser maior que 0")

if __name__ == '__main__':
    unittest.main()