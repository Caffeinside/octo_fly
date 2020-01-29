import sqlite3

import pandas as pd
from prefect import task

db_1_path = '../data/raw/batch_1.db'
db_2_path = '../data/raw/batch_2.db'

# TODO: can we include DB connections in prefect?

@task
def get_flights_data(db_1_path: str, db_2_path: str) -> pd.DataFrame:
    conn_1 = sqlite3.connect(db_1_path)
    conn_2 = sqlite3.connect(db_2_path)
    flights_1 = pd.read_sql_query("SELECT * FROM vols", conn_1)
    flights_2 = pd.read_sql_query("SELECT * FROM vols", conn_2)
    return pd.concat([flights_1, flights_2])


@task
def get_airports_data(db_path: str) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    return pd.read_sql_query("SELECT * FROM aeroports", conn)


@task
def get_airlines_data(db_path: str) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    return pd.read_sql_query("SELECT * FROM compagnies", conn)


@task
def get_fuel_data(path: str) -> pd.DataFrame:
    return pd.read_parquet(path)
