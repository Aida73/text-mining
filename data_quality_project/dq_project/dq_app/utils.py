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
from .scrapping import getCategories


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
    print(dataset_path)
    with open(dataset_path, 'r') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.readline())
        return dialect.delimiter


############################################## -CORRECTION-OF-GIVEN-DATAFRAME-##########################################################


def correct_target(dataset_path, target):
    dataset = read_dataset(dataset_path)
    column_target = dataset[target]
    column_target.dropna(inplace=True)
    target_dataset = pd.DataFrame({target: column_target.str.lower()})
    target1 = target_dataset.copy()[:20000].copy()
    print("---------------------------------------------------the correction starts--------------------------------------------")
    target1[target] = target1[target].str.lower(
    ).swifter.apply(clean_txt)
    target1['Corrected'] = target1[target].str.lower(
    ).swifter.apply(getCorrectWordTool)
    print(target1.head())
    return target1


def find_category(dataset: DataFrame, target: String, category: String):
    categories = getCategories(category)
    if isinstance(categories, str):
        print(
            f"{category} ne contient malheureusement aucun élément. Veuillez la supprimer ou la changer")
    else:
        categories.append(category.lower())
        if "Corrected" in dataset.columns:
            dataset['Corrected'] = dataset['Corrected'].swifter.apply(
                lambda x: correction(x, category))
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


def find_categories(dataset_corrected_path, target: String, categories: list) -> DataFrame:
    dataset = read_dataset(dataset_corrected_path)
    dataset_to_use = dataset.copy()
    print("--------------------------------------------finding categories----------------------------------------")
    for category in check_categories_searched(categories):
        find_category(dataset_to_use, target, category)
    dataset_to_use['Categorie'] = dataset_to_use['Categorie'].swifter.apply(
        refactor)
    return dataset_to_use


if __name__ == "__main__":
    args = sys.argv
    globals()[args[1]](*args[2:])
