from pandas.io import sql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix

#if you do not use linux, I'm sorry.
data_formated = pd.read_csv(r'../db/vagas_formated_data.csv', sep = ';')
data_general = pd.read_csv(r'../db/vagas_general_data.csv', sep = ';')

# Defining all the categories
categories = data_formated['Materia'].unique()
print(categories.shape)
print(data_formated['Descricao'].shape)


# Defining model
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# insert values to model
model.fit(data_formated['Descricao'], data_formated['Materia'])

# Try to predict general text
labels = model.predict(data_formated['Descricao'])

# Export to .csv file
pd.DataFrame(labels).to_csv(r'reports/lala.csv', sep=';')

print(labels)

mat = confusion_matrix(data_formated['Descricao'], labels)
#sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False
#            , xticklabels=data_formated['Materia']
#            , yticklabels=data_formated['Materia'])

#plt.xlabel('true label')
#plt.ylabel('predicted label')
#plt.show()