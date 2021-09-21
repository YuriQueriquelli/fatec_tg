import psycopg2
from config import config

def insert_cursos(cursos):
    sql = "INSERT INTO curso(curso_titulo) VALUES(%s)"
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.executemany(sql, cursos)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    insert_cursos([
        ('Análise e Desenvolvimento de Sistemas',),
        ('Comércio Exterior',),
        ('Gestão Empresarial',),
        ('Gestão de Serviços',),
        ('Logística Aeroportuária',),
        ('Redes de Computadores',),
        ('Indefinido',)
    ])