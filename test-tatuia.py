import unittest
import tatuia
import json
import src.connection.fretados_model as fretados_model
import src.connection.restaurante_model as restaurante_model



class Testtatuia(unittest.TestCase):
    """
        Todos os casos de testes devem ser escritos como funções
        que começam com test.
    """
    def test_welcome(self):
        """
            A ia deve retornar a intent correta
        """
        #restaurante_model.populate_database() # garante que o database foi populado
        try:
            result,intent = tatuia.tatu_zap.get_reply('olá tatu')
            self.assertEqual(intent, 'welcome',"Não apresentou a intent correta")
        except Exception as e:
            self.fail("A mensagem welcome não deve retornar Erro")

    def test_anything(self):
        """
            A ia deve retornar a intent correta
        """
        #restaurante_model.populate_database() # garante que o database foi populado
        try:
            result,intent = tatuia.tatu_zap.get_reply('qual o resultado do jogo do Brasil e Camarões')
            self.assertEqual(intent, 'anything_else',"Não apresentou a intent correta")
        except Exception as e:
            self.fail("A mensagem anything não deve retornar Erro")

    def test_myclasses(self):
        """
            A ia deve retornar a intent correta e a resposta deve ter os elementos esperados.
        """
        #restaurante_model.populate_database() # garante que o database foi populado
        try:
            result,intent = tatuia.tatu_zap.get_reply('qual as matérias do ra 11201721679')
            self.assertEqual(intent, 'myclasses',"Não apresentou a intent correta")
            self.assertGreaterEqual(result.find('Horário '), 0,"Não apresentou a lista de disciplinas esperadas")
        except Exception as e:
            self.fail("A mensagem myclasses não deve retornar Erro")

    def test_myclasses_notRA(self):
        """
            A ia deve retornar a intent correta e a resposta deve ter os elementos esperados.
        """
        #restaurante_model.populate_database() # garante que o database foi populado
        try:
            result,intent = tatuia.tatu_zap.get_reply('qual as matérias do ra ')
            self.assertEqual(intent, 'myclasses',"Não apresentou a intent correta")
            self.assertEqual(result, 'RA não encontrado, por favor digite seu RA',"Não apresentou a mensagem para quando não informou o RA.")
        except Exception as e:
            self.fail("A mensagem myclassesNRA não deve retornar Erro")

    def test_fretados(self):
        """
            A ia deve retornar a intent correta e a resposta deve ter os elementos esperados.
        """
        try:
            result,intent = tatuia.tatu_zap.get_reply('qual o próximo fretade de sa pra sbc')
            self.assertEqual(intent, 'businfo',"Não apresentou a intent correta")
            self.assertEqual(result.find('Linha:')!=-1 or result.find('fretado adequado')!=-1, True,"Não apresentou a mensagem para as fretados.\n"+result)
        except Exception as e:
            self.fail("A mensagem fretados não deve retornar Erro")

    def test_discinfo(self):
        """
            A ia deve retornar a intent correta e a resposta deve ter os elementos esperados.
        """

        try:
            result,intent = tatuia.tatu_zap.get_reply('quero saber a ementa de fisica quantica')
            print('res: ',result)
            self.assertEqual(intent, 'discinfo',"Não apresentou a intent correta")
            self.assertEqual(result.find('Ementa: Bases experimentais da Mecânica Quântica')!=-1,True,"Não apresentou a ementa para fisica quantica."+result)

        except Exception as e:
            self.fail("A mensagem discinfo não deve retornar Erro")
    def test_ru(self):
        """
            A ia deve retornar a intent correta e a resposta deve ter os elementos esperados.
        """
        try:
            result,intent = tatuia.tatu_zap.get_reply('quero saber qual ru')
            print('res: ',result)
            self.assertEqual(intent, 'ru',"Não apresentou a intent correta")
            self.assertEqual(result.find('O Restaurante Universitário não')!=(-1) or result.find('Prato Principal')!=(-1),True,"Não apresentou as mensagens esperadas para a intent do ru."+result)

        except Exception as e:
            self.fail("A mensagem ru não deve retornar Erro")

if __name__ == '__main__':
    unittest.main()