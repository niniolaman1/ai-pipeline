from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

def get_connection():
    conn = psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        dbname=os.environ["POSTGRES_DB"],
        user =os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )

    return conn
