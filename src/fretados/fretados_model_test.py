from copy import deepcopy
import unittest
from src.fretados.fretados_model import Fretado, list_all, insert_item, find_by_all_fields, populate_database, find_by_linha, insert_items

class TestFretadoModel(unittest.TestCase):
    """
        Todos os casos de testes devem ser escritos como funções
        que começam com test.
    """
    def test_list_all_len(self):
        """
            O list_all após população deve retornar ao menos 1 elemento
        """
        #populate_database() # garante que o database foi populado

        all_bus = list_all() # lista todos

        self.assertGreater(len(list(all_bus)), 0, "A lista deve ser não nula")

    def test_insert_item_inserts(self):
        """
            A função de inserção de um único elemento não deve retornar erros.
        """

        bus = Fretado(-1, "SEMANA", "SA", "07:07", "SBC", "07:17", 'N/A')

        try:
            insert_item(bus.to_dict())
        except Exception as e:
            self.fail("A inserção não deve retornar Erro")

    def test_insert_item_find(self):
        """
            Um elemento inserido deve ser recuperável sem retornar erros.
        """
        bus = Fretado(-1, "SEMANA", "SA", "07:07", "SBC", "07:17", 'N/A')

        try:
            insert_item(deepcopy(bus.to_dict()))

            find_by_all_fields(**(bus.to_dict()))
        except Exception as e:
            self.fail("Um elemento inserido deve ser recuperado sem erro")


    def test_insert_item_find_retrieve(self):
        """
            Um elemento inserido deve ser recuperado.
        """
        bus = Fretado(-1, "SEMANA", "SA", "07:07", "SBC", "07:17", 'N/A')

        insert_item(deepcopy(bus.to_dict()))

        response = find_by_all_fields(**(bus.to_dict()))

        bus_retrieved = Fretado.from_dict(list(response)[0])

        self.assertEqual(
            sorted(bus.to_dict().items()),
            sorted(bus_retrieved.to_dict().items()),
            "O elemento inserido deve ser igual ao recuperado",
        )

    def test_insert_items_inserts(self):
        """
            A função de inserção de multiplos elementos não deve retornar erros.
        """

        bus_1 = Fretado(-1, "SEMANA", "SA", "07:07", "SBC", "07:17", 'N/A').to_dict()

        bus_2 = Fretado(2, "SEMANA", "SBC", "08:07", "SA", "08:17", 'N/A').to_dict()

        try:
            insert_items([bus_1, bus_2])
        except Exception as e:
            self.fail("A inserção de multiplos elementos não deve retornar Erro")

    def test_find_by_linha_len(self):
        """
            Ao buscar um fretado de uma determinada linha
            num determinado dia da semana, devemos obter
            uma lista de fretados.
        """
        populate_database() # garante que o database foi populado
        day = 0 # indice da segunda-feira
        line = 1

        response = find_by_linha(line,day)

        self.assertGreater(len(list(response)), 0, "A lista de fretatos recuperados para uma linha valida deve ser maior que 0")

if __name__ == '__main__':
    unittest.main()
