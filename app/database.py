import psycopg2
from psycopg2.extras import RealDictCursor
import time
while True:
    try:
        conn=psycopg2.connect(host='localhost', database='fastapiapp', user='postgres', password='monkeyDluffy3!', cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection was successful")
        break
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        time.sleep(2)