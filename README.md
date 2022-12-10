# TatuZap

O TatuZap é um bot de WhatsApp, que tem como objetivo auxiliar os estudantes da UFABC à acessar dados cruciais para o cotidiano da faculdade, como dados da matrícula atual do aluno, salas, professores, matérias, entre outros.

O MVP do TatuZap consiste de dois repositórios, o ETLTatuZap, reponsável por carregar os dados da UFABC periodicamente e popular o banco de dados, e o BotTatuZap, que consiste na IA que será responsável por se comunicar com o usuário e recuperar os dados solicitados no banco já populado.

<hr />

## ETLTatuZap

Os códigos presentes nesse repositório são relativos ao processo de Extração, Transformação e Carregamento (LOAD), também conhecido como _ETL_, toda essa etapa tem como objetivo alimentar o banco de dados a ser utilizado em nosso chatbot (https://github.com/TatuZap/BotTatuZap) para responder queries de usuários.

Dentro do ETLTatuZap, pretendemos utilizar as seguintes tecnologias:

- Python(3.9)

- Pandas

- MongoDB

- FastAPI

<hr />

## Instruções de instalação

Passo a passo para rodar o projeto.

### Clonando o repositório:

- Clone o repositório do Tatuzap ETL

```sh
git clone git@github.com:TatuZap/ETLTatuZap.git
```

### Instalando python:

- Windows: download do [Instalador](https://www.python.org/downloads/)

- Linux: sudo apt-get install python3

### Instalando PIP

- Windows: curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
  python get-pip.py
- Linux: sudo apt install python3-pip
  Conferindo a instalação: pip3 --version

### Instalando virtualenv

- pip install virtualenv

#### Criando Ambiente Virtual

- python3 -m venv venv

#### Ativando ambiente virtual

- Windows: No CMD venv\Scripts\Activate

- Linux: source venv/bin/activate

### Instalando Dependencias

- pip install -r requirements.txt

<hr />

## Instruções de execução

### Funcionalidade de catalogo

- Rodar o comando `python3`
- Rodar o comando `import src.catalogo.catalogo_model as catalogo_model`
- Rodar o comando `catalogo_model.populate_database()` para raspar os dados e popular o banco
- Rodar o comando `list(catalogo_model.list_all())` por exemplo

### Funcionalidade de fretados

- Rodar o comando `python3`
- Rodar o comando `import src.fretados.fretados_model as fretados_model`
- Rodar o comando `fretados_model.populate_database()` para raspar os dados e popular o banco
- Rodar o comando `list(fretados_model.list_all())` por exemplo

### Funcionalidade de restaurante

- Rodar o comando `python3`
- Rodar o comando `import src.restaurante.restaurante_model as restaurante_model`
- Rodar o comando `restaurante_model.populate_database()` para raspar os dados e popular o banco
- Rodar o comando `list(restaurante_model.list_all())` por exemplo

### Funcionalidade de turmas

- Essa funcionalidade esta em refatoração, ainda não há instrucoes claras para rodar

### Funcionalidade de usuario

- Rodar o comando `python3`
- Rodar o comando `import src.usuario.usuario_model as usuario_model`
- Rodar o comando `list(usuario_model.list_all())` por exemplo

<hr />

## Instruções de testes automatizados

### Funcionalidade de catalogo

- Rodar o comando `python3 -m src.catalogo.catalogo_model_test`

### Funcionalidade de fretados

- Rodar o comando `python3 -m src.fretados.fretados_model_test`

### Funcionalidade de restaurante

- Rodar o comando `python3 -m src.restaurante.restaurante_model_test`

### Funcionalidade de turmas

- Ainda não há testes para essa funcionalidade

### Funcionalidade de usuario

- Rodar o comando `python3 -m src.restaurante.restaurante_model_test`
