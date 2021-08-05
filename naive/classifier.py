import model
from model import text_cleaning
from model import formula
import numpy as np
import pandas as pd
from csv import reader
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

#load general data as panda
df = pd.read_csv(r'reports/vagas_general_data.csv', sep = ';' )
df.head()

#give a number to any word
bow_transformer = CountVectorizer(analyzer=text_cleaning).fit(df['Descricao'])

#tranform all sentences into word number model like, (0, WordNumber) count
title_bow = bow_transformer.transform(df['Descricao'])

#transform a count matrix to a normalized
tfidf_transformer = TfidfTransformer(norm = 'l2', smooth_idf = True, sublinear_tf = False, use_idf = True).fit(title_bow)

#give importance value to each word in every sentence
title_tfidf = tfidf_transformer.transform(title_bow)

all_predictions = model.predict(title_tfidf)
print(all_predictions)
print(confusion_matrix(df['Materia'], all_predictions))

accuracy = accuracy_score(df['Materia'], all_predictions)
print(accuracy)