import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import pickle
import psycopg2
from instance.config import config

#save classifiers
def saveclassifier(model):
    try:
        f = open('my_classifier.pickle', 'wb')
        pickle.dump(model, f)
        f.close()
        print('Salvo com sucesso')
    except:
        print('Erro ao salvar o arquivo')

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
    
def main():  
    # load data  
    data_formated = postgresql_to_dataframe("SELECT c.curso_titulo, v.formatada_desc FROM vaga_formatada v INNER JOIN curso c ON c.curso_id = v.curso_id;", (r'curso_id', r'formatada_desc'))

    # Defining all the categories
    categories = data_formated['curso_id'].unique()

    # Defining base model
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())

    # insert values to model
    model.fit(data_formated['formatada_desc'], data_formated['curso_id'])

    # save model into a pickle file
    saveclassifier(model)

if __name__ == '__main__':
    main()