import psycopg2

conn = psycopg2.connect(host='localhost',
                        database='db_school', 
                        user='postgres', 
                        password='postgres',
                        port=5432)
