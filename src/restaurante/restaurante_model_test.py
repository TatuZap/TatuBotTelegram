import unittest
from copy import deepcopy
from src.restaurante.restaurante_model import list_all, insert_item, find_by_weekday_str, insert_items, RestauranteCardapio

class TestRestauranteModel(unittest.TestCase):
    """
        Todos os casos de testes devem ser escritos como funções
        que começam com test.
    """
    def test_list_all_len(self):
        """
            O list_all após população deve retornar ao menos 1 elemento
        """
        #populate_database() # garante que o database foi populado
        menus = list_all() # lista todos
        self.assertGreater(len(list(menus)), 0,"A lista deve ser não nula")

    def test_insert_item_inserts(self):
        """
            A função de inserção de um único elemento não deve retornar erros.
        """
        cardapio_domingo = RestauranteCardapio("26/11", "prato principal: pizza", "picanha", "de batata com cenoura", "Gelatina")

        try:
            insert_item(cardapio_domingo.to_dict())
        except Exception as e:
            print(e)
            self.fail("A inserção não deve retornar Erro")

    def test_insert_item_find(self):
        """
            Um elemento inserido deve ser recuperável sem retornar erros.
        """

        cardapio_domingo = RestauranteCardapio("26/11", "prato principal: pizza", "picanha", "de batata com cenoura", "Gelatina")

        try:
            insert_item(deepcopy(cardapio_domingo.to_dict()))
            find_by_weekday_str(cardapio_domingo.data,0)
            #self.assertGreater(len(list(response_find)), 0, "Ao inserir um elemento, este deve estar no banco.")
        except Exception as e:
            self.fail("Um elemento inserido deve ser recuperado sem erro")


    def test_insert_item_find_retrieve(self):
        """
            Um elemento inserido deve ser recuperado.
        """

        cardapio_domingo = RestauranteCardapio('30/11', 'Parmeggiana', 'Hamburguer', "de batata com cenoura", "Gelatina")

        insert_item(deepcopy(cardapio_domingo.to_dict()))
        response = find_by_weekday_str(cardapio_domingo.data,0)
        menu_retrieved = list(response)[0]
        del menu_retrieved["_id"] # deleta o atributo "_id" que vem do banco de dados e não usamos para nada
        self.assertEqual(sorted(cardapio_domingo.to_dict().items()), sorted(menu_retrieved.items()), "O elemento inserido deve ser igual ao recuperado")

    def test_insert_items_inserts(self):
        """
            A função de inserção de multiplos elementos não deve retornar erros.
        """
        cardapio_sabado = RestauranteCardapio('04/12', 'Nada', 'Vento', 'de batata com cenoura', 'Gelatina')
        cardapio_domingo = RestauranteCardapio('05/12', 'Hot dog', 'Macarronada', 'de batata com cenoura', 'Gelatina')

        try:
            response = insert_items([cardapio_sabado.to_dict(), cardapio_domingo.to_dict()])
        except Exception as e:
            self.fail("A inserção de multiplos elementos não deve retornar Erro")

if __name__ == '__main__':
    unittest.main()
