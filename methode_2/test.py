import pandas as pd
data = pd.read_csv("/Users/user/Downloads/corrected_profession.csv")

to_correct = input("entrer l'élément à corriger: ")
correction = input("Element de remplacement: ")

data.loc[data.Corrected == to_correct, "Corrected"] = correction
data.to_csv("/Users/user/Downloads/corrected_profession.csv")
