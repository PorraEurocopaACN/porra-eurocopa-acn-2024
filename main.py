from tournament.tournament_app import MyApp
from tournament.data_model import DataModel

data_model = DataModel()
data_model.hardcode_groups_table() # TODO: path until we upload all data

my_app = MyApp()
my_app.run()
