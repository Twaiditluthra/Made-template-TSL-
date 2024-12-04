import unittest
import os
import pandas as pd
import sqlite3
from pipeline import main  # Assuming your script is named pipeline.py

class TestDataPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Run the main function to execute the data pipeline
        main()

    def test_data_directory_exists(self):
        # Check if the data directory exists
        self.assertTrue(os.path.isdir("../data"), "Data directory does not exist")

    def test_csv_file_exists(self):
        # Check if the CSV output file exists
        self.assertTrue(os.path.isfile('../data/tourism_data.csv'), "CSV output file does not exist")

    def test_sqlite_file_exists(self):
        # Check if the SQLite database file exists
        self.assertTrue(os.path.isfile('../data/tourism_data.db'), "SQLite database file does not exist")

    def test_csv_file_content(self):
        # Load the CSV file and check if it has data
        df = pd.read_csv('../data/tourism_data.csv')
        self.assertFalse(df.empty, "CSV file is empty")
        self.assertTrue(len(df) > 0, "CSV file has no data rows")

    def test_sqlite_file_content(self):
        # Connect to the SQLite database and check if the table has data
        conn = sqlite3.connect('../data/tourism_data.db')
        query = "SELECT COUNT(*) FROM tourism_data"
        cursor = conn.cursor()
        cursor.execute(query)
        count = cursor.fetchone()[0]
        conn.close()
        self.assertTrue(count > 0, "SQLite database table 'tourism_data' is empty")

if __name__ == '__main__':
    unittest.main()
