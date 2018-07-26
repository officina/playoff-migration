from pprint import pprint
from dotenv import load_dotenv
import os
from pathlib import Path

from refactor_playoff_migration import GetPlayoffData
from playoff_migration import PlayoffMigration, Games

from playoff import Playoff

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
playoff_client = Playoff(
    client_id=os.environ["GAMELABNOTARGETV01_CLIENT_ID"],
    client_secret=os.environ["GAMELABNOTARGETV01_CLIENT_SECRET"],
    type='client',
    allow_unsecure=True
)

team_id = "globale"
player_id = "agazzani"

gp = GetPlayoffData(playoff_client)
pm = PlayoffMigration()


lead_by_id = pm.get_leaderboards_players(Games.original)

pprint(lead_by_id)
