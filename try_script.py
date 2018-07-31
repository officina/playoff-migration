from pprint import pprint
from dotenv import load_dotenv
import os
from pathlib import Path

from refactor_playoff_migration import *
from scoped_leaderboard import ScopedLeaderboard
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

playoff_client2 = Playoff(
    client_id=os.environ["GAMELABCLONSCOPED2_CLIENT_ID"],
    client_secret=os.environ["GAMELABCLONSCOPED2_CLIENT_SECRET"],
    type='client',
    allow_unsecure=True
)

design_getter = GetPlayoffDesign(playoff_client)

team_design = design_getter.get_single_team_design("globale")

pprint(team_design)

team_design2 = design_getter.get_single_team_design("")

pprint(team_design2)
