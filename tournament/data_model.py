import sqlite3
import os
import json
from pathlib import Path
import pandas as pd


class DataModel:
    """
    A class representing the data model for managing Eurocup 2024 predictions.
    """

    def __init__(self, populate_initial_tables: bool = False) -> None:
        """
        Initializes the DataModel class.

        Parameters:
        - populate_initial_tables (bool): Whether to populate initial tables upon initialization.
        """
        self.connect: sqlite3.Connection = sqlite3.connect("pwd.db")
        self.cursor: sqlite3.Cursor = self.connect.cursor()
        self.create_tables()
        self.select_all_from_tables()
        if populate_initial_tables:
            self.populate_initial_tables()

    def create_tables(self):
        """
        Creates necessary tables in the database if they do not exist.
        """
        # Get the path to the JSON file
        json_file_path = os.path.join(
            os.path.dirname(__file__), "tables_definition.json"
        )

        # Load the JSON file
        with open(json_file_path, "r") as f:
            table_definitions = json.load(f)["tables"]

        # Iterate over each table definition and create the tables
        for table_definition in table_definitions:
            table_name = table_definition["table_name"]
            columns = table_definition["columns"]
            primary_key = table_definition["primary_key"]

            column_definitions = ", ".join(
                [
                    f"{column['name']} {column['type']} {column['constraints']}"
                    for column in columns
                ]
            )
            primary_key_definition = (
                f", PRIMARY KEY ({', '.join(primary_key)})" if primary_key else ""
            )
            create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions}{primary_key_definition});"
            self.cursor.execute(create_table_sql)
        self.connect.commit()

    def populate_initial_tables(self):
        """
        Populates initial tables in the database upon initialization.
        """
        self.populate_groups_table()

    def populate_groups_table(self):
        """
        Populates the 'tbl_group_games' table with data from an Excel file uploaded within data folder.
        """
        games_calendar_path = os.path.join(
            Path(__file__).parent.parent, "data", "eurocup_games_calendar.xlsx"
        )
        df = pd.read_excel(games_calendar_path, sheet_name="group_stage")
        df.to_sql(
            name="tbl_group_games", con=self.connect, if_exists="replace", index=False
        )
        self.connect.commit()

    def select_all_from_tables(self):
        """
        Retrieves and prints all data from all tables in the database.
        """
        # Get the path to the JSON file
        json_file_path = os.path.join(
            os.path.dirname(__file__), "tables_definition.json"
        )

        # Load the JSON file
        with open(json_file_path, "r") as f:
            table_definitions = json.load(f)["tables"]

        # Iterate over each table definition and execute SELECT * query
        for table_definition in table_definitions:
            table_name = table_definition["table_name"]
            select_all_sql = f"SELECT * FROM {table_name};"
            self.cursor.execute(select_all_sql)
            rows = self.cursor.fetchall()
            print(f"Data from table {table_name}:")
            for row in rows:
                print(row)
