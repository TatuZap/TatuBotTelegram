import pandas as pd

def xlsx_to_df(file,sheetname):
    df = pd.read_excel(file,sheet_name=sheetname)
    return df