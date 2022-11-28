import unittest
import usuario_model
import json 


class TestUsuarioModel(unittest.TestCase):
    """
        Todos os casos de testes devem ser escritos como funções
        que começam com test.
    """
    def test_list_all_len(self):
        """
            O list_all após população deve retornar ao menos 1 elemento
        """
        all_user = usuario_model.list_all() # lista todos
        self.assertGreater(len(list(all_user)), 0," A lista deve ser não nula")

    def test_insert_item(self):
        """
            A inserção não deve retornar erros
        """
        user = {"ra":"11201722051","id":1}
        try:
            usuario_model.insert_item(json.loads(json.dumps(user)))
        except Exception as e:
            self.fail("Não deveria retornar erros")
    
    def test_find_by_id(self):
        """
            A busca deve retorna exatamente o mesmo elemento
        """
        user = {"ra":"11201810691","id":2}

        usuario_model.insert_item(json.loads(json.dumps(user)))
        retrieved_user = usuario_model.find_by_id(user["id"])
        del retrieved_user["_id"]
        self.assertEqual(sorted(json.loads(json.dumps(user)).items()), sorted(json.loads(json.dumps(retrieved_user)).items()), "O elemento inserido deve ser igual ao recuperado")


    def test_find_and_update(self):
        """
            A Atualização de um usuário não deve retornar erros
        """
        user = {"ra":"11201810691","id":10}
        try:
            usuario_model.insert_item(json.loads(json.dumps(user)))
            usuario_model.find_and_update(user["id"],"11201721679")
        except Exception as e:
            self.fail("Não deveria retornar erros")
        
    
    def test_find_and_update_updates(self):
        """
            A Atualização de um usuário não deve retornar erros
        """
        user = {"ra":"11201810691","id":1900}
        usuario_model.insert_item(json.loads(json.dumps(user)))
        usuario_model.find_and_update(user["id"],"1212121212")
        retrieved_user = usuario_model.find_by_id(user["id"])
        del retrieved_user["_id"]
        # minha vericação é nos campos
        diffs = 0
        for key in user.keys():
            if user[key] != retrieved_user[key]:
                diffs += 1
        
        self.assertEqual(diffs, 1, "O elemento modificado dista em apenas um campo")




if __name__ == '__main__':
    unittest.main()