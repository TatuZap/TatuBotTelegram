import random as random
#from random import choice


def fill_database(database, n):
    random.seed()
    for intent in database['intents']:
        
        if intent["tag"] == 'myclasses':
            # # sinonimo de QUERO
            # list1 = ['quero', 'desejo', 'pretendo', 'cogito', 'exijo', 'necessito', 'preciso', 'procuro', 'interesso-me','','informe','diga','qual é']+['']*10
            # # sinonimos de SABER
            # list2 = ['saber', 'entender', 'que me informe', 'conhecer', 'compreender']+['']*10
            # # variacoes para MINHAS TURMAS
            # list3 = ['minhas salas', 'minhas turmas', 'minha grade', 'minhas salas de aula', 'minhas classes', 'minha próxima aula', 'a próxima aula',
            #         'a turma seguinte', 'a seguinte sala', 'as salas', 'a sala','os professores','meus horários','minhas matérias','minha matérias','próximo professor','que sala devo ir']
            list1  = ['minhas', 'quero minhas', 'quais as minhas', 'qual minha', 'diga a ','informe a','quero saber as', 'me fale as','qual é', 'diz a']+['']*10
            list2   = ['materias', 'materia', 'sala','salas','professor','professora','professoras','docente','docentes','local','turma','turmas','professores','disciplinas','aula','aulas','grade','horario','horarios','classe','classes']
            list3 = ['agora','que devo ir','na segunda','na terca','na quarta','na quinta','na sexta','de manha','de tarde','de noite']+['']*7

            for i in range(n):
                a = random.choice(list1)+' '+random.choice(list2)+' '+random.choice(list3)
                if a not in intent['patterns'] and a != "  ":
                    intent['patterns'].append (a)
                else: i = i-1

        if intent["tag"] == 'businfo':
            # sinonimo de QUERO
            list_bus1 = ['quero', 'desejo', 'pretendo', 'necessito', 'preciso', 'procuro']+['']*6
            # sinonimos de SABER
            list_bus2 = ['saber', 'entender', 'me informar', 'conhecer']+['']*4
            # variacoes para QUE HORAS
            list_bus3 = ['que horas', 'que momento', 'quando']+['']*3
            # sinonimos de PARTIR
            list_bus4 = ['sai', 'parte']+['']*2
            # sinonimos de ONIBUS
            list_bus5 = ['o onibus', 'o busao', 'o fretado', 'o transporte', 'a lotação','o circular', 'os fretados','quero ir de fretado','de sa pra sbc','quero ir de sa']
            
            for i in range(n):
                a = random.choice(list_bus1)+' '+random.choice(list_bus2)+' '+random.choice(list_bus3)+' '+random.choice(list_bus4)+' '+random.choice(list_bus5)
                if a not in intent['patterns'] and a != "    ":
                    intent['patterns'].append (a)
                else: i = i-1                
                    
        if intent["tag"] == 'discinfo':
            list_disc1 = ['quero', 'desejo', 'pretendo', 'necessito', 'preciso', 'procuro']+['']*5
            list_disc2 = ['saber', 'entender', 'me informar', 'conhecer']+['']*3
            list_disc3 = ['ementa','plano de ensino','requisitos', 'bibliografia', 'disciplina']
            list_disc4 = ['da disciplina','da matéria','da cadeira','do curso','disciplina']+['']*4

            for i in range(n):
                a = random.choice(list_disc1)+' '+random.choice(list_disc2)+' '+random.choice(list_disc3)+' '+random.choice(list_disc4)
                if a != "   ":
                    intent['patterns'].append (a)
                
        if intent["tag"] == 'ru':
            list_disc1 = ['quero', 'desejo', 'pretendo', 'necessito', 'preciso', 'procuro']+['']*6
            list_disc2 = ['saber', 'entender', 'me informar', 'conhecer']+['']*4
            list_disc3 = ['o que será no almoço','o que será no jantar','qual o almoço','qual o jantar','qual a janta','o que tem de comida','o que tem de refeição', 'qual a refeição', 'o cardápio', 'o que temos no ru','o q tem pra comer','restaurante universiário','cardápio','qual a comida','o que tem pra almoçar','o que tem de janta']

            for i in range(n):
                a = random.choice(list_disc1)+' '+random.choice(list_disc2)+' '+random.choice(list_disc3)
                if a != "  ":
                    intent['patterns'].append (a)
                    
        if intent["tag"] == 'welcome':
            list_wel1 = ['oi','ola','salve','eae', 'hey', 'opa']+[""]*3
            list_wel2 = ['bom dia','boa tarde','boa noite', 'como vai', 'tudo bem', 'como voce esta']+[""]*3
            list_wel3 = ['bot','tatu','tatuzap']+[""]*3

            for i in range(n):
                a = random.choice(list_wel1)+' '+random.choice(list_wel2)+' '+random.choice(list_wel3)
                if a != "  ":
                    intent['patterns'].append (a)
                
    return database

def fill_treino(database, n):
    random.seed()
    for intent in database['intents']:
        if intent["tag"] == 'myclasses':
            list1  = ['minhas', 'quero minhas', 'quais as minhas', 'qual minha', 'diga a ','informe a','quero saber as', 'me fale as','qual é', 'diz a']+['']*10
            list2   = ['materias', 'materia', 'sala', 'disciplina','professor','local','turma','turmas','professores','disciplinas','salas','aula','aulas','grade','horario','classe','classes']
            list3 = ['agora','que devo ir','na segunda','na terca','na quarta','na quinta','na sexta','de manha','de tarde','de noite']+['']*7

            for i in range(n):
                a = random.choice(list1)+' '+random.choice(list2)+' '+random.choice(list3)
                if(a != "  "):
                    intent['patterns'].append (a)


        if intent["tag"] == 'businfo':
            list_bus1 = ['quero saber','informe','qual','que hora','quando','quando sai','quero que sai','vai sair', 'sairá']+['']*6
            list_bus2 = ['fretado','fretados','onibus','busao','lotação']
            
            for i in range(n):
                a = random.choice(list_bus1)+' '+random.choice(list_bus2)
                if(a != " "):
                    intent['patterns'].append (a)
                
        if intent["tag"] == 'discinfo':
            list_disc1 = ['quero saber','informe','qual','que']+['']*3
            list_disc2 = ['ementa','plano de ensino','requisitos', 'bibliografia']

            for i in range(n):
                a = random.choice(list_disc1)+' '+random.choice(list_disc2)
                if(a != " "):
                    intent['patterns'].append (a)
                
        if intent["tag"] == 'ru':
            list_disc1 = ['quero saber','informe', 'me diga', 'me fale']+['']*4
            list_disc2 = ['o que será no almoço','o que será no jantar','o que tem de comida', 'qual a refeição', 'o cardápio', 'o que temos no ru','ru','restaurante universiário','refeitório']

            for i in range(n):
                a = random.choice(list_disc1)+' '+random.choice(list_disc2)
                if(a != " "):
                    intent['patterns'].append (a)

        if intent["tag"] == 'welcome':
            list_wel1 = ['oi','ola','salve','eae', 'hey']+['']*4
            list_wel2 = ['bom dia','boa tarde','boa noite', 'como vai', 'tudo bem', 'como voce esta']+['']*5
            list_wel3 = ['bot','tatu','tatuzap']+['']*3

            for i in range(n):
                a = random.choice(list_wel1)+' '+random.choice(list_wel2)+' '+random.choice(list_wel3)
                if(a != " "):
                    intent['patterns'].append (a)
                
    return database

def gerar_anything(n):
    lista = []
    list1  = ['cachorro','esquilo','gato','camelo','cobra','tamandua','tatu','gaviao','bambi','touro','topeira']+['']*5
    list2   = ['voador','estiloso','esquisito','veloz','minha nossa','meus pets','de fogo','vingador','perneta']+['']*5
    list3 = ['de patinete','de patins','meu heroi','meu idolo','tchubilou','digdin','auu','dale do dele']+['']*7

    list_wel1 = ['oi','ola','salve','eae', 'hey']+['']*4
    list_wel2 = ['bom dia','boa tarde','boa noite', 'como vai', 'tudo bem', 'como voce esta']+['']*5
    list_wel3 = ['bot','tatu','tatuzap']+['']*3

    for i in range(n):
        a = random.choice(list1)+' '+random.choice(list2)+' '+random.choice(list3)
        if(a != ""):
            lista.append (a)
    return lista


def print_dict(my_dict):
    keys, values = zip(*my_dict.items())
    print ("keys : ", str(keys))
    print ("values : ", str(values))


database = {
    "intents": [
            {
                "tag": "welcome",
                "patterns": [],
                "responses": ["Olá, serei seu assistente virtual, em que posso te ajudar?","Salve, qual foi ?", "Manda pro pai, Lança a braba", "No que posso te ajudar ?"],
                "context": [""]
            },
            {
                "tag": "myclasses",
                "patterns": [],
                "responses": ["Entendi, você deseja saber suas salas","Você deseja saber suas salas ?", "Ah, você quer saber qual sala ? ", "Suas Aulas ?"],
                "context": [""]
            },
            {
                "tag": "businfo",
                "patterns": [],
                "responses": ["Esses são os horários dos fretados","Horarios dos fretados: ", "Ah, você quer saber o horário dos fretados"],
                "context": [""]
            },
            {
                "tag": "discinfo",
                "patterns": [],
                "responses": ['Informações da disciplina X','Para a disciplina Y, as informações são as seguintes: '],
                "context": [""]
            },
        {
                "tag": "ru",
                "patterns": [],
                "responses": ['O cárdapio de hoje é esse:','Para o almoço temos:', 'Para o jantar teremos:'], # provisório
                "context": [""]
            },
            {
                "tag": "anything_else",
                "patterns": [],
                "responses": ["Desculpa, não entendi o que você falou, tente novamente!","Não compreendi a sua solicitação, talvez eu possa te ajudar", "Por favor, digite novamente"],
                "context": [""]
            }
        ]
    }
# n = 15
# database =fill_treino(database, n)
# #print (database['intents'][4]['patterns'][0:10])



