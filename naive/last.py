from pandas.io import sql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

#if you do not use linux, I'm sorry...
data_formated = pd.read_csv(r'../db/vagas_formated_data.csv', sep = ';')
data_general = pd.read_csv(r'../db/vagas_general_data.csv', sep = ';')

# Defining all the categories
categories = data_formated['Materia'].unique()

# Defining base model
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# insert values to model
model.fit(data_formated['Descricao'], data_formated['Materia'])

# Try to predict general text
labels = model.predict(data_formated['Descricao'])

data_predict = pd.DataFrame(labels, columns={"Predict"})

# Save accuracy score of this actua sample
accuracy = accuracy_score(data_formated['Materia'], data_predict)

# New application of model, now to general data
labels = model.predict(data_general['Descricao'])

data_predict = pd.DataFrame(labels, columns={"Predict"})

# WIP -> concat and save new dataFrame,  problaby is going to be easyer to just save de predictions
#print(data_predict.head())

#result_final = pd.merge(data_general, data_predict)

#print(result_final.head())

# Export to .csv file
#pd.DataFrame(labels).to_csv(r'reports/lala.csv', sep=';')

#mat = confusion_matrix(data_formated['Descricao'], labels)
#sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False
#            , xticklabels=data_formated['Materia']
#            , yticklabels=data_formated['Materia'])

#plt.xlabel('true label')
#plt.ylabel('predicted label')
#plt.show()