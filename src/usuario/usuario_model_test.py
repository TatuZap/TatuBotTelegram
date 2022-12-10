import unittest
from copy import deepcopy
from src.usuario.usuario_model import list_all, insert_item, find_by_id, find_and_update, Usuario

class TestUsuarioModel(unittest.TestCase):
    """
        Todos os casos de testes devem ser escritos como funções
        que começam com test.
    """
    def test_list_all_len(self):
        """
            O list_all após população deve retornar ao menos 1 elemento
        """
        all_user = list_all() # lista todos
        self.assertGreater(len(list(all_user)), 0," A lista deve ser não nula")

    def test_insert_item(self):
        """
            A inserção não deve retornar erros
        """

        user = Usuario(123, '11201722051')

        try:
            insert_item(user.to_dict())
        except Exception as e:
            self.fail("Não deveria retornar erros")

    def test_find_by_id(self):
        """
            A busca deve retorna exatamente o mesmo elemento
        """

        user = Usuario(999, '11201722051')

        insert_item(deepcopy(user.to_dict()))
        retrieved_user = find_by_id(user.id)
        del retrieved_user["_id"]
        self.assertEqual(sorted(user.to_dict().items()), sorted(retrieved_user.items()), "O elemento inserido deve ser igual ao recuperado")


    def test_find_and_update(self):
        """
            A Atualização de um usuário não deve retornar erros
        """

        user = Usuario(546, '11201722051')

        try:
            insert_item(deepcopy(user.to_dict()))
            find_and_update(user.id,"11201721679")
        except Exception as e:
            self.fail("Não deveria retornar erros")


    def test_find_and_update_updates(self):
        """
            A Atualização de um usuário não deve retornar erros
        """

        user = Usuario(948, '11201722051')

        insert_item(deepcopy(user.to_dict()))
        find_and_update(user.id, "1212121212")
        retrieved_user = find_by_id(user.id)
        del retrieved_user["_id"]
        # minha vericação é nos campos
        diffs = 0
        for key in user.to_dict().keys():
            if user.to_dict()[key] != retrieved_user[key]:
                diffs += 1

        self.assertEqual(diffs, 1, "O elemento modificado dista em apenas um campo")

if __name__ == '__main__':
    unittest.main()
