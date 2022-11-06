import os
import pandas as pd
from .system_separator import sep as sep

def files():
    path=os.path.realpath('./src/extract/turmas/files')
    files_name=os.listdir(path)
    files = []
    for file in files_name: files.append(path + sep() +file)
    return files

def file_output():
    path=os.path.realpath('./src/transform/turmas/output')
    files_name=os.listdir(path)
    files = []
    for file in files_name: files.append(path + sep() +file)
    return files

