import pandas as pd
import streamlit as st
from tournament.tournament_config.config import Config
from tournament.io_methods import IO


class MyApp:
    def __init__(self, config: Config):
        self.config = config
        self.title = "Eurocup 2024"
        self.io = IO(config)
        self.username = None
        self.user_input = None

    def run(self):
        self.render_title()
        self.render_content()
        self.username_textbox()
        self.create_user_input()
        self.export_user_input()

    def render_title(self):
        st.title(self.title)

    def render_content(self):
        st.write("This is a simple object-oriented Streamlit app. HOLAAAAAA")
        st.write("You can add more content and functionality here.")

    def username_textbox(self):
        self.username = st.text_area("Accenture user_id (e.g., john.simmons)", "")
        st.write("You entered: ", self.username)

    def create_user_input(self):
        self.user_input = pd.DataFrame.from_dict({"username": [self.username]})

    def export_user_input(self):
        self.io.write_to_excel(
            self.user_input, f"{self.config._output}/{self.username}.xlsk"
        )
