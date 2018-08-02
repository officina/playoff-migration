from pprint import pprint
from dotenv import load_dotenv
import os
from pathlib import Path

from refactor_playoff_migration import *
from scoped_leaderboard import ScopedLeaderboard
from playoff_migration import PlayoffMigration, Games
from playoff_migration_file import *

from playoff import Playoff


playoff_client = Utility.get_playoff_client(
    "GAMELABNOTARGETV01_CLIENT_ID",
    "GAMELABNOTARGETV01_CLIENT_SECRET"
)

playoff_client2 = Utility.get_playoff_client(
    "GAMELABCLONSCOPED2_CLIENT_ID",
    "GAMELABCLONSCOPED2_CLIENT_SECRET"
)

export_design = ExportDesign()

export_design.export_teams_design()
export_design.export_metric_design()
export_design.export_actions_design()
export_design.export_leaderboards_design()
