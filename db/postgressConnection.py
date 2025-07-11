import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

databseName = os.getenv("POSTGRESS_DATABSE_NAME")
hostName = os.getenv("POSTGRESS_HOST_NAME")
portName = os.getenv("POSTGRESS_PORT")
userName = os.getenv("POSTGRESS_USER_NAME")
dbPassword = os.getenv("POSTGRESS_PASSWORD")

print("Databse Name:", databseName)

def get_connection():
    try:
        connection = psycopg2.connect(
            database=databseName,
            user=userName,
            password=dbPassword,
            host=hostName,
            port=portName,
        )

        cursor = connection.cursor()
        print("Postgres connection established successfully.")
        return connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)


def close_connection(connection, cursor):
    if connection:
        cursor.close()
        connection.close()
        print("Postgres connection closed.")
