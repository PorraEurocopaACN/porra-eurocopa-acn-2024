import sqlite3
import os
import json


class DataModel:
    def __init__(self):
        self.connect = sqlite3.connect("pwd.db")
        self.cursor = self.connect.cursor()
        self.create_tables()
        self.select_all_from_tables() # TODO: remove

    def create_tables(self):
        # Get the path to the JSON file
        json_file_path = os.path.join(os.path.dirname(__file__), "tables_definition.json")

        # Load the JSON file
        with open(json_file_path, 'r') as f:
            table_definitions = json.load(f)["tables"]

        # Iterate over each table definition and create the tables
        for table_definition in table_definitions:
            table_name = table_definition["table_name"]
            columns = table_definition["columns"]
            primary_key = table_definition["primary_key"]

            column_definitions = ', '.join(
                [f"{column['name']} {column['type']} {column['constraints']}" for column in columns])
            primary_key_definition = f", PRIMARY KEY ({', '.join(primary_key)})" if primary_key else ""
            create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions}{primary_key_definition});"
            self.cursor.execute(create_table_sql)
            print(f"Created table {table_name}")
        self.connect.commit()

    def select_all_from_tables(self):
        # Get the path to the JSON file
        json_file_path = os.path.join(os.path.dirname(__file__), "tables_definition.json")

        # Load the JSON file
        with open(json_file_path, 'r') as f:
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

    def hardcode_groups_table(self):
        self.cursor.execute("DELETE FROM tbl_actual_groups;")

        hardcoded_data = [
            {"group_name": "A", "country": "Germany"},
            {"group_name": "A", "country": "Scotland"},
            {"group_name": "A", "country": "Hungary"},
            {"group_name": "A", "country": "Switzerland"},
            {"group_name": "B", "country": "Spain"},
            {"group_name": "B", "country": "Croatia"},
            {"group_name": "B", "country": "Italy"},
            {"group_name": "B", "country": "Albania"}
        ]
        for row in hardcoded_data:
            placeholders = ', '.join(['?' for _ in row.keys()])
            insert_sql = f"INSERT INTO tbl_actual_groups ({', '.join(row.keys())}) VALUES ({placeholders});"
            self.cursor.execute(insert_sql, list(row.values()))
        self.connect.commit()
