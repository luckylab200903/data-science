import os
import pandas as pd


script_dir = os.getcwd()
excel_file = os.path.join(script_dir, "Input.xlsx")
df = pd.read_excel(excel_file)
print(df)

