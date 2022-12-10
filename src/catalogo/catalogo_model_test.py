import unittest
from copy import deepcopy
from src.catalogo.catalogo_model import populate_database, list_all, find_by_apelido, find_by_sigla, insert_item, insert_items, delete_all, CatalogoDisciplina

class TestCatalogoModel(unittest.TestCase):
  """
      Todos os casos de testes devem ser escritos como funções
      que começam com test.
  """

  def test_list_all(self):
    """
        O list_all após população deve retornar ao menos 1 elemento
    """
    populate_database() # garante que o database foi populado
    all_classes = list_all() # lista todos

    self.assertGreater(len(list(all_classes)), 0,"A lista deve ser não nula")

  def test_find_by_apelido(self):
    """
        O método find_by_apelido deve achar a disciplina com o apelido indicado
    """
    populate_database() # garante que o database foi populado
    apelido = "bm"
    find_by_apelido_result = find_by_apelido(apelido)

    self.assertEqual(list(find_by_apelido_result)[0]['disciplina'], 'Bases Matematicas', "Deveria ter achado a matéria pelo apelido")

  def test_find_by_sigla(self):
    """
        O método find_by_sigla deve achar a sigla com o apelido indicado
    """
    populate_database() # garante que o database foi populado
    sigla = "BIS0003-15"
    find_by_sigla_result = find_by_sigla(sigla)

    self.assertEqual(list(find_by_sigla_result)[0]['disciplina'], 'Bases Matematicas', "Deveria ter achado a matéria pela sigla")

  def test_insert_item_inserts(self):
    """
        A função de inserção de um único elemento não deve retornar erros.
    """
    disciplina = CatalogoDisciplina('Sigla teste', 'Disciplina teste', 'TPI teste', "Recomendações teste", "Objetivos teste", "Ementa teste", "Apelido teste")
    
    try:
        insert_item(disciplina.to_dict())
    except Exception as e:
        self.fail("A inserção não deve retornar Erro")

  def test_insert_item_find(self):
    """
        Um elemento inserido deve ser recuperável sem retornar erros.
    """
    disciplina = CatalogoDisciplina('Sigla teste', 'Disciplina teste', 'TPI teste', "Recomendações teste", "Objetivos teste", "Ementa teste", "Apelido teste")

    try:
      insert_item(disciplina.to_dict())
      find_by_sigla(disciplina.sigla)
      find_by_apelido(disciplina.apelido)
    except Exception as e:
      self.fail("Um elemento inserido deve ser recuperado sem erro")


  def test_insert_item_find_retrieve(self):
    """
        Um elemento inserido deve ser recuperado.
    """

    disciplina = CatalogoDisciplina('Sigla teste', 'Disciplina teste', 'TPI teste', "Recomendações teste", "Objetivos teste", "Ementa teste", "Apelido teste")

    insert_item(deepcopy(disciplina.to_dict()))
    searched_class = find_by_sigla(disciplina.sigla)

    class_retrieved = list(searched_class)[0]

    del class_retrieved["_id"] # deleta o atributo "_id" que vem do banco de dados
    
    self.assertEqual(
      sorted(disciplina.to_dict().items()),
      sorted(class_retrieved.items()),
      "O elemento inserido deve ser igual ao recuperado",
    )

  def test_insert_items_inserts(self):
    """
        A função de inserção de multiplos elementos não deve retornar erros.
    """

    disciplinaA = CatalogoDisciplina('Sigla teste A', 'Disciplina teste A', 'TPI teste A', "Recomendações teste A", "Objetivos teste A", "Ementa teste A", "Apelido teste A")

    disciplinaB = CatalogoDisciplina('Sigla teste B', 'Disciplina teste B', 'TPI teste B', "Recomendações teste B", "Objetivos teste B", "Ementa teste B", "Apelido teste B")

    try:
      insert_items([disciplinaA.to_dict(), disciplinaB.to_dict()])
    except Exception as e:
      self.fail("A inserção de multiplos elementos não deve retornar Erro")

  def test_delete_all(self):
    """
        A função de delecao de todos os elementos deve deixar o banco vazio.
    """
    delete_all()

    self.assertEqual(list(list_all()), [], "Ao deletar tudo deve ficar vazio")

    populate_database()
    return

  def test_populate_database(self):
    """
        A função de popular o banco deixar o banco com todos os elementos.
    """
    delete_all()

    populate_database()

    self.assertGreater(len(list(list_all())), 0, "A lista deve ser não nula")
    return

if __name__ == '__main__':
  unittest.main()
