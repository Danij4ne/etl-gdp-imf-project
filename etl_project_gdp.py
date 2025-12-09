import requests 
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3 
import numpy as np 
from datetime import datetime  
import os

# Information Extraction
def extract(url, table_attribs):

    response = requests.get(url)
    response.raise_for_status()
    data = BeautifulSoup(response.text, "html.parser")

    df = pd.DataFrame(columns=table_attribs)

    tables = data.find_all("tbody")
    rows = tables[2].find_all("tr")

    for row in rows:
        col = row.find_all("td")
        if len(col) != 0:
            if col[0].find("a") is not None and "—" not in col[2].text:
                data_dict = {
                    "Country": col[0].a.contents[0],
                    "GDP_USD_millions": col[2].contents[0],
                }
                df1 = pd.DataFrame(data_dict, index=[0])
                df = pd.concat([df, df1], ignore_index=True)
    return df


# Information Transform
def transform(df: pd.DataFrame) -> pd.DataFrame:
    gdp_list = df["GDP_USD_millions"].astype(str).tolist()
    gdp_list = [float(x.replace(",", "")) for x in gdp_list]
    gdp_list = [np.round(x / 1000, 2) for x in gdp_list]

    df["GDP_USD_millions"] = gdp_list
    df = df.rename(columns={"GDP_USD_millions": "GDP_USD_billions"})

    return df


# Information Load
def load_to_csv(df: pd.DataFrame, csv_path: str) -> None:
    df.to_csv(csv_path, index=False)


def load_to_db(df: pd.DataFrame, sql_connection: sqlite3.Connection, table_name: str) -> None:
    df.to_sql(table_name, sql_connection, if_exists="replace", index=False)


def run_query(query_statement: str, sql_connection: sqlite3.Connection) -> None:
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)


def log_progress(message: str) -> None:
    timestamp_format = "%Y-%m-%d %H:%M:%S"
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open("logs/etl_project_log.txt", "a", encoding="utf-8") as f:
        f.write(timestamp + " : " + message + "\n")


# Logging Utility

def log_progress(message):
    # Ensure log directory exists
    os.makedirs("logs", exist_ok=True)

    timestamp_format = "%Y-%m-%d %H:%M:%S"
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)

    with open("logs/etl_project_log.txt", "a", encoding="utf-8") as f:
        f.write(timestamp + " : " + message + "\n")



# Main ETL Workflow


if __name__ == "__main__":
    
    url = "https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
    table_attribs = ["Country", "GDP_USD_millions"]
    db_name = "World_Economies.db"
    table_name = "Countries_by_GDP"
    csv_path = "Countries_by_GDP.csv"

    log_progress("Preliminaries completed. Starting ETL process.")

 
    df_extracted = extract(url, table_attribs)
    log_progress("Data extraction completed. Starting transformation.")

     
    df_transformed = transform(df_extracted)
    log_progress("Data transformation completed. Starting load process.")

    
    df_transformed.to_csv(csv_path, index=False)
    log_progress("Data saved to CSV file.")

     
    conn = sqlite3.connect(db_name)
    log_progress("SQL connection initiated.")

     
    load_to_db(df_transformed, conn, table_name)
    log_progress("Data loaded into database table. Running query.")

   
    query = f"SELECT * FROM {table_name} WHERE GDP_USD_billions >= 100"
    run_query(query, conn)

    log_progress("Process completed.")
    conn.close()
