"""
    Rode esse script somente uma vez para baixar os pré-requisitos
    que permitem o uso da biblioteca NLTK (natural language toolkit).
"""

import nltk
import warnings
from nltk import download
download(['punkt','averaged_perceptron_tagger','stopwords','wordnet','omw-1.4'])
stopwords = nltk.corpus.stopwords.words('portuguese')
warnings.filterwarnings('ignore')