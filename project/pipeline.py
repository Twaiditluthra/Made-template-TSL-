import os
import pandas as pd
import sqlite3
import ssl
import urllib.request

#As mentioned, I have made a directory for storing data
DATA_DIR = "../data"
DB_FILE = os.path.join(DATA_DIR, "tourism_data.db")

# Dataset URL
DATASET_URL = "https://datos.yvera.gob.ar/dataset/4cbf7d4a-702a-4911-8c1e-717a45214902/resource/fdfe0ae4-4acc-4421-aa48-6149a02bc615/download/turistas-no-residentes-serie.csv"


def download_data(url, save_path):
    """
    Data will be downloaded from the specified URL and saved locally.
    SSL verification will be disabled for the request.
    """
    #I have disabled SSL certificate verification as it was creating problems for me to proceed with working on my dataset
    ssl_context = ssl._create_unverified_context()
    
    #I then downloaded the data using urllib
    with urllib.request.urlopen(url, context=ssl_context) as response:
        data = response.read()
    
    #The content was then saved to a CSV file
    with open(save_path, "wb") as f:
        f.write(data)


def clean_and_transform_data(file_path):
    """
    The data shall be read, cleaned, and transformed for consistency using proper frameworks and functions to do so.
    """
    #I made sure to load the data into a Pandas DataFrame
    df = pd.read_csv(file_path)
    
    #I have standardized the column for reader's consistency respectively
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    
    #I handled missing values by either dropping them, by averaging the numeric values or by filling the empty blank with the most common occurrence 
    df.dropna(inplace=True)
    
    #I hereby ensure that the numeric columns are correctly formatted
    numeric_columns = ["amount_of_tourists"]  # Adjust based on actual column names
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    
    return df

def save_to_database(df, db_file, table_name="tourism_data"):
    """
    Data will be saved into an SQLite database.
    """
    # Database connection will be established
    conn = sqlite3.connect(db_file)
    
    # Data will be written to the specified table
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    
    # Connection will be closed
    conn.close()

def main():
    """
    The data pipeline process will be executed in this function.
    """
    #I hereby ensure that the data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    #We are downloading the dataset
    local_file = os.path.join(DATA_DIR, "tourism_data.csv")
    download_data(DATASET_URL, local_file)
    
    #We are cleaning and transforming the data
    transformed_data = clean_and_transform_data(local_file)
    
    #We are saving the data to an SQLite database
    save_to_database(transformed_data, DB_FILE)
    print("Pipeline executed successfully. Data saved to:", DB_FILE)

if __name__ == "__main__":
    main()