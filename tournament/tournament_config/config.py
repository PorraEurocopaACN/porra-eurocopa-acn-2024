import json
import getpass
from typing import Dict, Any


class Config:
    """
    Config class for reading and managing project configuration from a JSON file.

    Attributes:
        config_file_path (str): The path to the configuration JSON file.

    Methods:
        load_config(): Load configuration data from the specified JSON file.
    """

    def __init__(self, config_file_path: str):
        config_data = self.load_config(config_file_path)
        self._main_path = (
            f"C:/users/{getpass.getuser()}/{config_data['directories']['main_path']}"
        )
        self._eurocup = f"{self._main_path}/{config_data['directories']['eurocup']}"
        self._output = f"{self._eurocup}/{config_data['directories']['output']}"

    @staticmethod
    def load_config(config_file_path: str) -> Dict[str, Any]:
        try:
            with open(config_file_path, "r") as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            print("Config file not found. Make sure it exists at the specified path.")
            return {}
