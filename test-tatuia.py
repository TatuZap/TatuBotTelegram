import unittest
import tatuia
import json 


class Testtatuia(unittest.TestCase):
    """
        Todos os casos de testes devem ser escritos como funções
        que começam com test.
    """
    def test_welcome(self):
        """
            O list_all após população deve retornar ao menos 1 elemento
        """
        #restaurante_model.populate_database() # garante que o database foi populado
        try:
            result,intent = tatuia.tatu_zap.get_reply('olá tatu')
            self.assertEqual(intent, 'welcome',"Não apresentou a intent correta")
        except Exception as e:
            print(e)
            self.fail("A mensagem não deve retornar Erro")

    def test_anything(self):
        """
            O list_all após população deve retornar ao menos 1 elemento
        """
        #restaurante_model.populate_database() # garante que o database foi populado
        try:
            result,intent = tatuia.tatu_zap.get_reply('qual o resultado do jogo do Brasil e Camarões')
            self.assertEqual(intent, 'anything_else',"Não apresentou a intent correta")
        except Exception as e:
            print(e)
            self.fail("A mensagem não deve retornar Erro")

    # def test_insert_item_inserts(self):
    #     """
    #         A função de inserção de um único elemento não deve retornar erros.
    #     """
    #     sunday_menu = {
    #         "data": "26/11",
    #         "dia_semana": 6,
    #         "almoço": "prato principal: pizza",
    #         "jantar": "picanha",
    #         "saladas": "de batata com cenoura",
    #         "sobremesas": "Gelatina"}
    #     try:
    #         restaurante_model.insert_item(json.loads(json.dumps(sunday_menu)))
    #     except Exception as e:
    #         print(e)
    #         self.fail("A inserção não deve retornar Erro")
    
    # def test_insert_item_find(self):
    #     """
    #         Um elemento inserido deve ser recuperável sem retornar erros.
    #     """
    #     sunday_menu = {'data': '26/11',
    #         'dia_semana': 6,
    #         'almoço': 'RAviole',
    #         'jantar': 'picanha',
    #         'saladas': 'de batata com cenoura',
    #         'sobremesas': 'Gelatina'}
    #     try:
    #         restaurante_model.insert_item(json.loads(json.dumps(sunday_menu)))
    #         restaurante_model.find_by_weekday_str(sunday_menu["data"],0)
    #         #self.assertGreater(len(list(response_find)), 0, "Ao inserir um elemento, este deve estar no banco.")
    #     except Exception as e:
    #         self.fail("Um elemento inserido deve ser recuperado sem erro")


    # def test_insert_item_find_retrieve(self):
    #     """
    #         Um elemento inserido deve ser recuperado.
    #     """
    #     sunday_menu = {'data': '30/11',
    #         'dia_semana': 2,
    #         'almoço': 'Parmeggiana',
    #         'jantar': 'Hamburguer',
    #         'saladas': 'de batata com cenoura',
    #         'sobremesas': 'Gelatina'}

    #     restaurante_model.insert_item(json.loads(json.dumps(sunday_menu)))
    #     response = restaurante_model.find_by_weekday_str(sunday_menu["data"],0)
    #     menu_retrieved = list(response)[0]
    #     del menu_retrieved["_id"] # deleta o atributo "_id" que vem do banco de dados e não usamos para nada
    #     self.assertEqual(sorted(json.loads(json.dumps(sunday_menu)).items()), sorted(json.loads(json.dumps(menu_retrieved)).items()), "O elemento inserido deve ser igual ao recuperado")

    # def test_insert_items_inserts(self):
    #     """
    #         A função de inserção de multiplos elementos não deve retornar erros.
    #     """
    #     saturday_menu = {'data': '04/12',
    #         'dia_semana': 2,
    #         'almoço': 'Nada',
    #         'jantar': 'Vento',
    #         'saladas': 'de batata com cenoura',
    #         'sobremesas': 'Gelatina'}
    #     sunday_menu = {'data': '05/12',
    #         'dia_semana': 2,
    #         'almoço': 'Hot dog',
    #         'jantar': 'Macarronada',
    #         'saladas': 'de batata com cenoura',
    #         'sobremesas': 'Gelatina'}
    #     menus = [ json.loads(json.dumps(menus)) for menus in [saturday_menu,sunday_menu]]
    #     try:
    #         response = restaurante_model.insert_items(menus)
    #     except Exception as e:
    #         self.fail("A inserção de multiplos elementos não deve retornar Erro")

if __name__ == '__main__':
    unittest.main()