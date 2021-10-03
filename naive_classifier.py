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
import pickle
import psycopg2
from instance.config import config


def saveclassifier():
    f = open('my_classifier.pickle','rb')
    classifier = pickle.load(f)
    classifier.train()
    f.close()

#Transform a SELECT query into a pandas dataframe
def postgresql_to_dataframe(select_query, column_names):
    conn = None
    try:
        params =  config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cur.close()
        return 1
        
    tupples = cur.fetchall()
    cur.close()
    return pd.DataFrame(tupples, columns=column_names)

#Update table vaga_geral
def table_update(url, previsao):
    if previsao == 'Análise e Desenvolvimento de Sistemas':
        previsao = 1
    elif previsao == 'Comércio Exterior':
        previsao = 2
    elif previsao == 'Gestão Empresarial':
        previsao = 3
    elif previsao == 'Gestão de Serviços':
        previsao = 4
    elif previsao == 'Logística Aeroportuária':
        previsao = 5
    elif previsao == 'Redes de Computadores':
        previsao == 6
    else:
        return 1
    
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("""UPDATE vaga_geral SET curso_id = %s WHERE geral_url = %s""",(previsao, url))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cur.close()
        return 2
    finally:
        if conn is not None:
            conn.close()
    
data_formated = postgresql_to_dataframe("SELECT c.curso_titulo, v.formatada_desc FROM vaga_formatada v INNER JOIN curso c ON c.curso_id = v.curso_id;", (r'curso_id', r'formatada_desc'))
data_geral = postgresql_to_dataframe("SELECT geral_url, geral_desc FROM vaga_geral WHERE curso_id = 7;", (r'geral_url', r'geral_desc'))  

# Defining all the categories
categories = data_formated['curso_id'].unique()

# Defining base model
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# insert values to model
model.fit(data_formated['formatada_desc'], data_formated['curso_id'])

# New application of model, now to general data
#labels = model.predict(data_geral['geral_desc'])

for index, row in data_geral.iterrows():
    text = row['geral_desc']
    previsao = model.predict([text])
    previsao = str(previsao).replace("'", "").replace("[", "").replace("]", "")
    table_update(row['geral_url'], previsao)
    print(previsao , row['geral_url'])   
    


# WIP -> concat and save new dataFrame,  problaby is going to be easyer to just save de predictions
#print(data_predict.head())

#result_final = dp.merge(data_general, data_predict)

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