from config import host, user, password, db_name, port
import psycopg2


def database_checker(start_word, end_word):
    try:
        # Connect to exist database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port
        )

        # Execute a SELECT query to retrieve all rows from the 'users' table
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM wikiracing WHERE First_Step = "
                           f"'{start_word}' AND Second_Step = '{end_word}' "
                           f"OR Third_Step = '{end_word}'")

            # Fetch all the rows and Return the results
            rows = cursor.fetchall()
            if rows:
                return list(rows[0][1:rows[0].index(end_word) + 1])
            else:
                return False

    except Exception as ex:
        print(f"[INFO] Error: {ex}")

    finally:
        if connection:
            connection.close()


def database_creation():
    try:
        # Connect to exist database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port
        )

        # Autocommit for database
        connection.autocommit = True

        # Create a cursor
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS wikiracing(
                id serial PRIMARY KEY,
                First_Step varchar(50),
                Second_Step varchar(50),
                Third_Step varchar(50),
                Page_IN varchar(50),
                Links_IN INTEGER,
                Page_OUT varchar(50),
                Links_OUT INTEGER
            )""")

    except Exception as ex:
        print(f"[INFO] Error: {ex}")

    finally:
        if connection:
            connection.close()


def database_filling(wiki_path):
    try:
        # Connect to exist database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port
        )

        # Autocommit for database
        connection.autocommit = True

        if len(wiki_path) == 6:
            # Insert data into a "titles"
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                    INSERT INTO wikiracing (First_Step, Second_Step, Page_IN, 
                    Links_IN, Page_OUT, Links_OUT) VALUES(
                        '{wiki_path[0]}', '{wiki_path[1]}', '{wiki_path[2]}',
                        '{wiki_path[3]}', '{wiki_path[4]}','{wiki_path[5]}'
                )""")
        
        elif len(wiki_path) == 7:
            # Insert data into a "titles"
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                    INSERT INTO wikiracing (First_Step, Second_Step, 
                    Third_Step, Page_IN, Links_IN, Page_OUT, Links_OUT) VALUES(
                        '{wiki_path[0]}', '{wiki_path[1]}', '{wiki_path[2]}', 
                        '{wiki_path[3]}','{wiki_path[4]}', '{wiki_path[5]}', 
                        '{wiki_path[6]}'
                )""")

    except Exception as ex:
        print(f"[INFO] Error: {ex}")

    finally:
        if connection:
            connection.close()
