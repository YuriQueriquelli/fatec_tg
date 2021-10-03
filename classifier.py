from naive_bayes import postgresql_to_dataframe
import pickle
import psycopg2
from instance.config import config

def de_para_previsao(previsao):
    return {
        'Análise e Desenvolvimento de Sistemas':1,
        'Comércio Exterior':2,
        'Gestão Empresarial':3,
        'Gestão de Serviços':4,
        'Logística Aeroportuária':5,
        'Redes de Computadores':6
    }[previsao]

# update table vagas_geral
def table_update(url, previsao):

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

def main():
    #load data
    data_geral = postgresql_to_dataframe("SELECT geral_url, geral_desc FROM vaga_geral WHERE curso_id = 7;", (r'geral_url', r'geral_desc'))  

    # Open pickle file
    f = open('my_classifier.pickle', 'rb')
    classifier = pickle.load(f)
    f.close()


    for index, row in data_geral.iterrows():
        text = row['geral_desc']
        previsao = classifier.predict([text])
        previsao = str(previsao).replace("'", "").replace("[", "").replace("]", "")
        table_update(row['geral_url'], de_para_previsao(previsao))
        print(de_para_previsao(previsao) , row['geral_url'])   

if __name__ == '__main__':
    main()