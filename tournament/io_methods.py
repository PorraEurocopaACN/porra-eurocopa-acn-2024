import json
from typing import List, Union, Literal
import pandas as pd
from tournament.tournament_config.config import Config


class IO:
    """
    Responsible to manage input/output sources, mainly read and write from Disk

    """

    def __init__(self, config: Config):
        self._config = config

    def read_data_control(self, data_control_tab: str) -> pd.DataFrame:
        """
        Read data control file

        Args:
            data_control_tab (str): tab name

        Returns:
            dataframe: where `sources` are the input source tables, `fields` are the selected
            fields by source table with an alias and `types` are the field types by transformed table of the data model
        """
        return self.read_excel(
            filepath=self._config.data_control_filepath,
            sheet_name=data_control_tab,
            types=str,
        )

    @staticmethod
    def read_csv(
        filepath: str,
        sep: str = ",",
        parse_dates: List[str] = None,
        types: Union[type, dict] = None,
        skiprows: int = None,
    ) -> pd.DataFrame:
        """
        Read a CSV file and create a dataframe to store it

        Args:
            filepath (str): filepath of the csv to be read
            sep (str): column separator character
            parse_dates (list): date columns to be parsed
            types (dict): types of columns
            skiprows (int): rows to skip at the start of the file

        Returns:
            pd.DataFrame: file read
        """
        return pd.read_csv(
            filepath, sep=sep, parse_dates=parse_dates, dtype=types, skiprows=skiprows
        )

    @staticmethod
    def read_excel(
        filepath: str,
        sheet_name: str,
        parse_dates: List[str] = None,
        types: Union[type, dict] = None,
        skiprows: int = None,
    ) -> pd.DataFrame:
        """
        Read a CSV file and create a dataframe to store it

        Args:
            filepath (str): filepath of the csv to be read
            sheet_name (str): column separator character
            parse_dates (list): date columns to be parsed
            types (type or dict): types of columns
            skiprows (int): rows to skip at the start of the file

        Returns:
            pd.DataFrame: file read
        """
        return pd.read_excel(
            filepath,
            sheet_name=sheet_name,
            parse_dates=parse_dates,
            dtype=types,
            skiprows=skiprows,
        )

    @staticmethod
    def read_sql(query: str, connection) -> pd.DataFrame:
        """
        Execute query in given database and create a dataframe to store it

        Args:
            query (str): sql query
            connection (): database connection

        Returns:
            pd.DataFrame: file read
        """
        return pd.read_sql(sql=query, con=connection)

    @staticmethod
    def write_to_csv(df: pd.DataFrame, filepath: str) -> None:
        """
        Write a given dataframe `df` to CSV file

        Args:
            df (pd.DataFrame): dataframe to be written
            filepath (str): filepath where the file will be written
        """
        df.to_csv(filepath, index=False)

    @staticmethod
    def write_to_excel(
        df: pd.DataFrame, filepath: str, sheet_name: str = "Sheet1"
    ) -> None:
        """
        Write a given dataframe `df` to Excel file

        Args:
            df (pd.DataFrame): dataframe to be written
            filepath (str): filepath where the file will be written
            sheet_name (str): name of sheet of the excel where the file will be written
        """
        df.to_excel(f"{filepath}.xlsx", sheet_name, index=False)

    @staticmethod
    def write_to_excel_sheets(
        dfs: List[pd.DataFrame], filepath: str, sheet_names: List[str]
    ) -> None:
        """
        Write a given list of dataframes `dfs` to Excel file with given sheet_names `sheet_names`.

        Args:
            dfs (List[pd.DataFrame]): list of dataframes to be written
            filepath (str): filepath where the file will be written
            sheet_names (List[str]): list of names of sheets of the excel
        """
        writer = pd.ExcelWriter(filepath, engine="xlsxwriter")

        for idx, df in enumerate(dfs):
            df.to_excel(writer, sheet_name=sheet_names[idx], index=False)

        writer.close()

    @staticmethod
    def write_to_sql(
        df: pd.DataFrame,
        name: str,
        connection,
        schema: str = None,
        if_exists: str = "replace",
    ) -> None:
        """
        Write a given dataframe `df` to given database

        Args:
            df (pd.DataFrame): dataframe to be written
            name (str): name of SQL table
            connection : database connection
            schema (str): schema name
            if_exists (Literal): how to behave if table already exists
        """
        df.to_sql(
            name=name, con=connection, schema=schema, if_exists=if_exists, index=False
        )

    @staticmethod
    def write_json(d: dict, filepath: str) -> None:
        """
        Write a given dictionary in JSON format

        Args:
            d (dict): dataframe to be written
            filepath (str): filepath where the file will be written
        """
        with open(f"{filepath}", "w") as outfile:
            json.dump(d, outfile, indent=4)

    def delete_where_tbl(self, engine, tbl) -> None:
        """
        Deletes the input table for the current run id.
        Args:
            engine: sql engine
            tbl: tbl name that has to be deleted.

        Returns: None
        """
        # Create a database connection and execute the delete statement
        with engine.begin() as connection:
            connection.execute(tbl.delete().where(tbl.c.run_id == self._config.run_id))
