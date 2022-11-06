all: install

PYTHON_VERSION = 3.8 # change this variable to your currently python version between (>= 3.8 < 3.10 ) only. 
install:
	python$(PYTHON_VERSION) -m pip install enelvo  # this may be slow
	python$(PYTHON_VERSION) -m pip install nltk
	python$(PYTHON_VERSION) -m pip install -U spacy
	python$(PYTHON_VERSION) -m pip install unidecode 
	python$(PYTHON_VERSION) -m spacy download pt_core_news_lg
	python$(PYTHON_VERSION) -m pip install tensorflow
	python$(PYTHON_VERSION) -m pip install sklearn
	python$(PYTHON_VERSION) -m pip install pandas
	python$(PYTHON_VERSION) -m pip install matplotlib


	