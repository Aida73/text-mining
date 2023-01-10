"""
LanguageTool: is an open-source grammar tool, also known as the spellchecker for OpenOffice.
    This library allows you to detect grammar errors and spelling mistakes through a Python script or 
    through a command-line interface. We will work with the language_tool_pyton python package which can 
    be installed with the pip install language-tool-python command. By default, language_tool_python will 
    download a LanguageTool server .jar and run that in the background to detect grammar errors locally.
    However, LanguageTool also offers a Public HTTP Proofreading API that is supported as well but there
    is a restriction in the number of calls.
    We can directly use the correct funstion which Automatically apply suggestions to the text.
Swifter:  is a package that tries to efficiently apply any function to a Pandas Data Frame 
or Series object in the quickest available method
"""
################################################# TEXT-MINING########################################################
import sys
import os
import datetime
import language_tool_python
import pandas as pd
import csv
import swifter
import nltk
from pygments.token import String
from pandas.core.groupby.grouper import DataFrame
from scrapping import getCategories


tool = language_tool_python.LanguageTool(
    'fr', config={'cacheSize': 2000, 'pipelineCaching': True})


def read_dataset(dataset_path):
    if not dataset_path.endswith('.csv'):
        print("Il faut un fichier csv !")
        exit
    else:
        separator = find_delimiter(dataset_path)
        dataset = pd.read_csv(dataset_path, sep=separator)
        return dataset


def clean_txt(word):
    cleaned = word.translate(
        {ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
    return cleaned


def getCorrectWordTool(word):
    return tool.correct(clean_txt(word))


def correction(ligne, category):
    corrected = []
    for elt in ligne.split(" "):
        if nltk.edit_distance(elt, category) <= 2:
            corrected.append(category)
        else:
            corrected.append(elt)
    return " ".join(corrected)


"""this function return a dataframe with two columns: the target (ex:profession) and a column named Corrected"""


def find_delimiter(dataset_path):
    with open(dataset_path, 'r') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.readline())
        return dialect.delimiter

############################################## -CORRECTION-OF-GIVEN-DATAFRAME-##########################################################


def correct_target(dataset_path, target):
    dataset = read_dataset(dataset_path)
    column_target = dataset[target]
    column_target.dropna(inplace=True)
    target_dataset = pd.DataFrame({target: column_target.str.lower()})
    target1 = target_dataset.copy()[:2000].copy()
    print("---------------------------------------------------the correction starts--------------------------------------------")
    target1[target] = target1[target].str.lower(
    ).swifter.apply(clean_txt)
    target1['Corrected'] = target1[target].str.lower(
    ).swifter.apply(getCorrectWordTool)
    print(target1.head())
    choice = input("Tapeze 1 pour enregistrer la base et 0 pour quitter: ")
    while choice not in ["0", "1"]:
        print("Vous ne pouvez choisir qu'entre 0 et 1 !")
        choice = input(
            "Tapeze 1 pour enregistrer la base et 0 pour quitter: ")
    if choice == "1":
        name = input("Donner le nom du dataset : ")
        save_to_csv(target1, name)
        print("Enregistrer ! ")
        return target1
    else:
        return target1
        exit


"""This function is used in order to find the dataframe's elements that belong to an given Category
Algo: for each row in the dataframe, if any word belong to the webScrapping'returned list, this one is labelling with the category given"""


def find_category(dataset: DataFrame, target: String, category: String):
    categories = getCategories(category)
    if isinstance(categories, str):
        print(
            f"{category} ne contient malheureusement aucun élément. Veuillez la supprimer ou la changer")
    else:
        categories.append(category.lower())
        if "Corrected" in dataset.columns:
            dataset['Corrected'] = dataset['Corrected'].swifter.apply(
                lambda x: correction(x, category))  # this is not applied
            if "Categorie" not in dataset.columns:
                dataset['Categorie'] = "None,"
            dataset.loc[dataset['Corrected'].str.lower().swifter.apply(lambda x: any(
                [k in x.split(" ") for k in categories])) == True, 'Categorie'] += category+","
        else:
            print("Verifier si la colonne Corrected existe")


def check_categories_searched(categories: list):
    correct_categories = []
    for cat in categories:
        correct_categories.append(tool.correct(cat))
    return correct_categories


def refactor(x):
    value = set(x.split(","))
    value.discard("")
    if len(value) > 1:
        value.discard("None")
    return ",".join(value)


def getCliCategories():
    categ = []
    forward = True
    while forward:
        if len(categ) == 0:
            choice = input("Tapeze 1 ajouter une categorie: ")
        else:
            choice = input(
                "Tapeze 1 ajouter une autre catégorie categorie ou 0 pour la classification: ")
        while choice not in ["1", "0"]:
            print("Vous ne pouvez choisir qu'entre 0 et 1 !")
            if len(choice) > 0:
                choice = input(
                    "Tapeze 1 ajouter une autre catégorie categorie ou 0 pour la classification: ")
            else:
                choice = input("Tapeze 1 ajouter une categorie: ")
        if choice == "1":
            categorie = input("categorie : ")
            categ.append(categorie)
            print(categ)
        if choice == "0":
            forward = False
            print(categ)

    return categ


"""This function is used in order to apply the find_category function to an  entire list of categories
It returns a dataframe with three column: the target one, another named Corrected and the column Categorie"""

############################################## -FIND-CATEGORIES-OF-GIVEN-DATAFRAME-##########################################################


def find_categories(dataset_corrected_path, target: String) -> DataFrame:
    dataset = read_dataset(dataset_corrected_path)
    dataset_to_use = dataset.copy()
    cliCategories = getCliCategories()
    print("--------------------------------------------finding categories----------------------------------------")
    for category in check_categories_searched(cliCategories):
        find_category(dataset_to_use, target, category)
    dataset_to_use['Categorie'] = dataset_to_use['Categorie'].swifter.apply(
        refactor)
    choice = input("Tapeze 1 pour enregistrer la base et 0 pour quitter: ")
    while choice not in ["0", "1"]:
        print("Vous ne pouvez choisir qu'entre 0 et 1 !")
        choice = input(
            "Tapeze 1 pour enregistrer la base et 0 pour quitter: ")
    if choice == "1":
        name = input("Donner le nom du dataset : ")
        save_to_csv(dataset_to_use, name)
        print("Enregistrer ! ")
        return get_categories_value_counts(dataset_to_use, 'Categorie')
    else:
        return dataset_to_use
        exit


"""this function will save the dataframe to csv in the current path"""

############################################## -SAVE-GIVEN-DATAFRAME-##########################################################


def save_to_csv(dataframe, name):
    home = os.path.expanduser("~")
    path = os.path.join(home, "Downloads")
    os.chdir(path)
    dataframe.to_csv(f"{name}.csv")


""""will be use to count differents values to a given column in the dataframe"""

############################################## -CATEGORIES-VALUES-COUNT-##########################################################


def get_categories_value_counts(dataframe, column):
    if column not in dataframe.columns:
        print(f"{column} n'est pas présente dans {dataframe}")
    else:
        print(dataframe[column].value_counts())


def correct_outliers(dataset_path, target):
    dataset = read_dataset(dataset_path)
    to_correct = input("Entrer l'élément à corriger: ")
    correction = input("Elément de remplacement: ")
    if target not in dataset.columns:
        print(
            f"Verifiez la target car {target} ne se trouve pas dans ce dataset")
    else:
        dataset.loc[dataset[target] == to_correct, target] = correction
        name = input("Donner le nom du dataset pour l'enregistrer: ")
        save_to_csv(dataset, name)
        print("Enregistrer ! ")


if __name__ == "__main__":
    args = sys.argv
    globals()[args[1]](*args[2:])
