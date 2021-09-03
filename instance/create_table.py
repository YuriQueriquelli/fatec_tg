import psycopg2
from config import config

def create_tables():
    commands = (
    """
    DROP TABLE IF EXISTS materias;
    """,
    """
    DROP TABLE IF EXISTS vaga_formatada;
    """,
    """
    DROP TABLE IF EXISTS vaga_geral;
    """,
    """
        CREATE TABLE materias(
            materia_id INT GENERATED ALWAYS AS IDENTITY,
            materia_titulo VARCHAR(50) NOT NULL,
            PRIMARY KEY(materia_id)
        )
        """,
        """
        CREATE TABLE vaga_formatada(
            formatada_url VARCHAR(255) NOT NULL,
            formatada_titulo VARCHAR NOT NULL,
            formatada_desc VARCHAR NOT NULL,
            materia_id INT NOT NULL,
            PRIMARY KEY(materia_id),
                FOREIGN KEY(materia_id)
                    REFERENCES materias(materia_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE vaga_geral (
            geral_url VARCHAR(255) NOT NULL,
            geral_titulo VARCHAR NOT NULL,
            geral_cargo VARCHAR NOT NULL,
            geral_desc VARCHAR NOT NULL,
            geral_data DATE,
            materia_id INT NOT NULL,
            PRIMARY KEY(materia_id),
                FOREIGN KEY(materia_id)
                    REFERENCES materias(materia_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
    conn = None

    try: 
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        for command in commands:
            cur.execute(command)

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_tables()