import utils
import pandas as pd
"""
data = pd.read_csv(
    '/Users/user/Desktop/text-mining/VariableCibles.csv', sep=";")


# Correct dataframe
target4 = utils.correct_target(data, "profession")

# correct manually some outliers
target2 = target4.copy()
target2.loc[target4['Corrected'] == 'élevé', 'Corrected'] = "élève"


#find one category elements
print(utils.find_category(target2.copy(), "ménagère"))"""


# data = pd.read_csv(
#    '/Users/user/Desktop/text-mining/VariableCibles.csv', sep=";")
data = pd.read_csv("/Users/user/Downloads/symptomes.csv")

data_corrected = utils.correct_target(data, "autres_1")


# data_corrected2 = data_corrected.copy()
# ----------correct some outliers-----------------
# data_corrected2.loc[data_corrected2['Corrected']
#                     == 'élevé', 'Corrected'] = "élève"

# print(data_corrected2)

# trouver les categories
# categorized = utils.find_categories(
#    data_corrected2, ["commercantttefteg"])

categorized_dataset = utils.find_categories(
    data_corrected, "autres_1", ['rhinorrhee', 'douleurs musculaires', 'anosmie'])

print(utils.get_categories_value_counts(categorized_dataset, "Categorie"))
