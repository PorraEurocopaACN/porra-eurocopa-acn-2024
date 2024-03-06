import streamlit as st
import webbrowser
import sqlite3
from tournament.data_model import DataModel
import pandas as pd
from itertools import combinations


class MyApp:
    def __init__(self):
        self.title = "SC&OA Eurocup 2024"
        self.stage_groups = "Stage Groups"
        self.user_id = None
        self.page_icon = "🚀"
        self.data_model = DataModel()

    def run(self):
        self.set_initial_page()
        radio_option = self.set_basic_properties()

        if radio_option == "Predictions":
            self.set_stage_groups_bet()
            # Text input for user ID
            self.user_id = st.text_input("Enter User ID:")
            games_df = self.select_group()
            self.bet_games(games_df)

        if radio_option == "Results":
            st.subheader("Results 🗝️")
            self.display_all_bets()

        if radio_option == "GenAI":
            st.subheader("GenAI 🔄")

    def set_basic_properties(self):
        st.title("Eurocup 2024 ⚽")
        radio_option = st.sidebar.radio("Menu", options=["Predictions", "Results", "Gen AI"])
        return radio_option


    def set_initial_page(self):
        st.set_page_config(page_title=self.title, page_icon=self.page_icon)

    def set_stage_groups_bet(self):
        st.subheader("Stage Groups ⚽")

    def get_unique_group_names(self):
        self.data_model.cursor.execute("SELECT DISTINCT group_name FROM tbl_actual_groups;")
        return [row[0] for row in self.data_model.cursor.fetchall()]

    def select_group(self):
        group_names = self.get_unique_group_names()
        # Create a selectbox widget to choose group names
        selected_group = st.selectbox("Select a group name:", group_names)
        query = f"SELECT * FROM tbl_actual_groups WHERE group_name = '{selected_group}';"
        self.data_model.cursor.execute(query)
        results = self.data_model.cursor.fetchall()
        column_names = [description[0] for description in self.data_model.cursor.description]
        df = pd.DataFrame(results, columns=column_names)
        games_df = self.generate_game_combinations(df, selected_group)
        st.table(games_df)
        return games_df

    def generate_game_combinations(self, df, selected_group):
        game_combinations = []
        countries = df[df['group_name'] == selected_group]['country'].tolist()
        group_combinations = list(combinations(countries, 2))
        game_combinations.extend(group_combinations)
        games_df = pd.DataFrame(game_combinations, columns=['Local', 'Visitor'])
        return games_df

    def bet_games(self, games_df):
        with st.form(key='game_result_form'):
            # Define a dictionary to map game IDs to local and visitor teams
            game_teams_map = {f"{local}-{visitor}": (local, visitor) for local, visitor in
                              games_df[['Local', 'Visitor']].values}
            # Select game
            selected_game_id = st.selectbox("Select a game:", list(game_teams_map.keys()))

            # Get local and visitor teams based on selected game ID
            local, visitor = game_teams_map[selected_game_id]

            # Set result
            local_score = st.number_input("Local Score", min_value=0, step=1)
            visitor_score = st.number_input("Visitor Score", min_value=0, step=1)

            print(f"local: {local}")
            print(f"visitor: {visitor}")
            print(f"local_score: {local_score}")
            print(f"visitor_score: {visitor_score}")

            # Submit button
            submitted = st.form_submit_button("Submit")

        # If form is submitted, update the database with the result
        if submitted:
            # Update the database with the result
            self.data_model.cursor.execute(f"INSERT INTO tbl_user_predictions values (:user_id, :local, :visitor, :local_goals, :visitor_goals)",
                           (self.user_id, local, visitor, local_score, visitor_score))
            self.data_model.connect.commit()
            st.success("Result updated successfully!")

        self.data_model.select_all_from_tables()

    def display_all_bets(self):
        # Execute SQL query to retrieve all records from tbl_user_predictions
        self.data_model.cursor.execute("SELECT * FROM tbl_user_predictions")
        results = self.data_model.cursor.fetchall()

        # Display the results in a table
        if results:
            # Get column names
            column_names = [description[0] for description in self.data_model.cursor.description]

            # Create a DataFrame from the results
            import pandas as pd
            df = pd.DataFrame(results, columns=column_names)

            # Display the DataFrame as a table
            st.write("All Bets:")
            st.table(df)
        else:
            st.write("No bets found.")

