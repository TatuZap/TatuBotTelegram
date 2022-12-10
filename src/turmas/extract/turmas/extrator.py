from .get_files import files
from .xlsx_to_df import xlsx_to_df
from .system_separator import sep as sep

def get_all_dataframes():
    dfs = []
    for file in files():
        file_name = file.split(sep())[-1]
        data = {
            "file_name": file_name,
            "df" : xlsx_to_df(file,'AJUSTE_2022.3')
        }
        dfs.append(data)
    return dfs

