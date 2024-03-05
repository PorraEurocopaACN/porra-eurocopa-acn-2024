from tournament.tournament_config.config import Config
from tournament.tournament_app import MyApp
from pathlib import Path
from os.path import join

project_root: str = Path(__file__).parent
config: Config = Config(
    join(project_root, "./tournament/tournament_config/config_data.json")
)
my_app: MyApp = MyApp(config=config)
my_app.run()
