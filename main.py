from tournament.tournament_app import MyApp
from tournament.data_model import DataModel

POPULATE_INITIAL_TABLES = False
data_model = DataModel(populate_initial_tables=POPULATE_INITIAL_TABLES)

my_app = MyApp()
my_app.run()
