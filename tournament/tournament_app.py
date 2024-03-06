import streamlit as st
import webbrowser
import sqlite3
from tournament.data_model import DataModel, DataValidator
import pandas as pd
from typing import Optional


class MyApp:
    """
    A class representing the Streamlit application for managing Eurocup 2024 predictions.
    """

    def __init__(self):
        """
        Initializes the MyApp class.
        """
        self.title: str = "SC&OA Eurocup 2024"
        self.stage_groups: str = "Stage Groups"
        self.user_id: Optional[str] = None
        self.page_icon: str = "🚀"
        self.data_model: DataModel = DataModel()
        self.data_validator: DataValidator = DataValidator(data_model=self.data_model)

    def run(self) -> None:
        """
        Runs the Streamlit application.
        """
        self.set_initial_page_interface()
        radio_option = self.set_basic_properties_interface()
        if radio_option == "Predictions":
            self.create_predictions_tab()
        if radio_option == "Results":
            st.subheader("Results 🗝️")
            self.display_all_bets()
        if radio_option == "GenAI":
            st.subheader("GenAI 🔄")

    def create_predictions_tab(self) -> None:
        """
        Creates the predictions tab.
        """
        self.set_stage_groups_interface()
        # Text input for user ID
        self.user_id = st.text_input("Enter User ID:")
        games_df = self.select_group()
        self.predict_games(games_df)

    def set_basic_properties_interface(self) -> str:
        """
        Sets the basic properties interface.

        Returns:
        - str: The selected radio option.
        """
        st.title("Eurocup 2024 ⚽")
        radio_option = st.sidebar.radio(
            "Menu", options=["Predictions", "Results", "Gen AI"]
        )
        return radio_option

    def set_initial_page_interface(self) -> None:
        """
        Sets the initial page interface.
        """
        st.set_page_config(page_title=self.title, page_icon=self.page_icon)

    def set_stage_groups_interface(self) -> None:
        """
        Sets the stage groups interface.
        """
        st.subheader("Stage Groups ⚽")

    def get_unique_group_names(self) -> list[str]:
        """
        Retrieves unique group names from the database.

        Returns:
        - list[str]: A list of unique group names.
        """
        self.data_model.cursor.execute(
            "SELECT DISTINCT group_name FROM tbl_group_games;"
        )
        return [row[0] for row in self.data_model.cursor.fetchall()]

    def select_group(self) -> pd.DataFrame:
        """
        Selects a group from the database.

        Returns:
        - pd.DataFrame: DataFrame containing the selected group data.
        """
        group_names = self.get_unique_group_names()
        # Create a selectbox widget to choose group names
        selected_group = st.selectbox("Select a group name:", group_names)
        query = f"SELECT * FROM tbl_group_games WHERE group_name = '{selected_group}';"
        self.data_model.cursor.execute(query)
        results = self.data_model.cursor.fetchall()
        column_names = [
            description[0] for description in self.data_model.cursor.description
        ]
        df = pd.DataFrame(results, columns=column_names)
        st.table(df)
        return df

    def predict_games(self, games_df: pd.DataFrame) -> None:
        """
        Predicts the outcome of games.

        Parameters:
        - games_df (pd.DataFrame): DataFrame containing game data.
        """
        with st.form(key="game_result_form"):
            # Define a dictionary to map game IDs to local and visitor teams
            game_teams_map = {
                f"{local}-{visitor}": (local, visitor)
                for local, visitor in games_df[["local", "visitor"]].values
            }
            # Select game
            selected_game_id = st.selectbox(
                "Select a game:", list(game_teams_map.keys())
            )
            # Get local and visitor teams based on selected game ID
            local, visitor = game_teams_map[selected_game_id]
            # Set result
            local_score = st.number_input("Local Score", min_value=0, step=1)
            visitor_score = st.number_input("Visitor Score", min_value=0, step=1)
            # Submit button
            submitted = st.form_submit_button("Submit")

        # If form is submitted, update the database with the result
        if submitted:
            if self.user_id != "":
                if self.data_validator.check_duplicate_prediction(
                    self.user_id, local, visitor
                ):
                    self.data_model.cursor.execute(
                        """
                        UPDATE tbl_user_predictions 
                        SET local_goals = ?, visitor_goals = ? 
                        WHERE user_id = ? AND local = ? AND visitor = ?
                        """,
                        (local_score, visitor_score, self.user_id, local, visitor),
                    )
                else:
                    # Update the database with the result
                    self.data_model.cursor.execute(
                        f"INSERT INTO tbl_user_predictions values (:user_id, :local, :visitor, :local_goals, :visitor_goals)",
                        (self.user_id, local, visitor, local_score, visitor_score),
                    )
                self.data_model.connect.commit()
                st.success("Result updated successfully! ✅")
            else:
                st.error(
                    f"You need to populate your user_id if you want to submit a prediction. 🌚"
                )
        self.data_model.select_all_from_tables()

    def display_all_bets(self) -> None:
        """
        Displays all bets made by users.
        """
        # Execute SQL query to retrieve all records from tbl_user_predictions
        self.data_model.cursor.execute("SELECT * FROM tbl_user_predictions")
        results = self.data_model.cursor.fetchall()

        # Display the results in a table
        if results:
            # Get column names
            column_names = [
                description[0] for description in self.data_model.cursor.description
            ]
            df = pd.DataFrame(results, columns=column_names)

            # Display the DataFrame as a table
            st.write("All Bets:")
            st.table(df)
        else:
            st.write("No bets found.")
