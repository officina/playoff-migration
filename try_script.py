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

post_design = PostPlayoffDesign(playoff_client2)

data = {
    'id': 'globale_creativita',
    'name': 'Globale Creatività',
    'entity_type': 'players',
    'scope': {
        'type': 'team_definition',
        'id': 'globale'
    },
    'metric': {
        'id': 'creativita',
        'type': 'point'
    }
}

post_design.create_leaderboard_design(data)
