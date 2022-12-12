# TatuZap

O TatuZap é um bot de Telegram, que tem como objetivo auxiliar os estudantes da UFABC à acessar dados cruciais para o cotidiano da faculdade, como dados da matrícula atual do aluno, salas, professores, matérias, entre outros.

O MVP do TatuZap consiste de três repositórios:

- [ETLTatuZap](https://github.com/TatuZap/ETLTatuZap), reponsável por carregar os dados da UFABC periodicamente e popular o banco de dados,
- [BotTatuZap](https://github.com/TatuZap/BotTatuZap), que consiste na IA que será responsável por se comunicar com o usuário e recuperar os dados solicitados no banco já populado
- [TatuBotTelegram](https://github.com/TatuZap/TatuBotTelegram), que é o resultado provisório da integração entre os dois mencionados acima

<hr />

## TatuBotTelegram

Os códigos presentes nesse repositório são relativos a integração provisória entre os repositórios [ETLTatuZap](https://github.com/TatuZap/ETLTatuZap) e [BotTatuZap](https://github.com/TatuZap/BotTatuZap) para o funcionamento completo do bot TatuZap, além da integração com o Telegram.

<hr />

## Instruções de instalação

Passo a passo para rodar o projeto.

### Clonando o repositório:

- Clone o repositório do Tatuzap TatuBotTelegram

```sh
git clone git@github.com:TatuZap/TatuBotTelegram.git
```

### Instalando python:

OBS.: Nesse repositório, o por conta de subdepencias (mais especificamente o ENELVO) somos obrigados a utilizar python 3.8.

Para instalar no Ubuntu:

```sh
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.8
```

### Instalando distutils

```sh
sudo apt install python3.8-distutils
```

### Instalando Dependencias

```sh
make
```

### Fazendo Setup do nltk

```sh
python3.8 nltksetup.py
```

<hr />

## Instruções de execução no CLI do python

**OBS.: Para que as instruções de execução funcionem, é necessário adicionar as variáveis de ambiente corretas (assim como exemplificado em .env.example) em um arquivo .env na pasta raiz do projeto**

```sh
python3.8
```

Isso roda a IA no CLI do python, porem não testa o bot do Telegram em conjunto com ela.

Dentro do python CLI rodar:
- `import tatuia`
- `tatuia.tatu_zap.get_reply('ola')`
- `tatuia.tatu_zap.get_reply('quero minhas turmas 11201810247')`
- `tatuia.tatu_zap.get_reply('quero saber sobre o ru')`
- `tatuia.tatu_zap.get_reply('Quero saber a ementa de Engenharia de Software')`
- `tatuia.tatu_zap.get_reply('quanto falta pro quad acabar')`

<hr />

## Instruções de execução no Telegram

- Gerar a chave do Telegram via Bot Father
- Adicionar a chave no arquivo .env
- Rodar `python3.8 tatutelegram.py`

## Instruções de testes automatizados

```sh
python3.8 test-tatuia.py
```
