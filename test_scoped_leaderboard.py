import unittest

from refactor_playoff_migration import *
from scoped_leaderboard import *

from playoff import Playoff, PlayoffException
from dotenv import load_dotenv


class ScopedLeaderboardTest(unittest.TestCase):

    def setUp(self):
        from pathlib import Path
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)
        original = Playoff(
            client_id=os.environ["GAMELABNOTARGETV01_CLIENT_ID"],
            client_secret=os.environ["GAMELABNOTARGETV01_CLIENT_SECRET"],
            type='client',
            allow_unsecure=True
        )
        to_clone = Playoff(
            client_id=os.environ["GAMELABCLONSCOPED2_CLIENT_ID"],
            client_secret=os.environ["GAMELABCLONSCOPED2_CLIENT_SECRET"],
            type='client',
            allow_unsecure=True
        )

        self.scoped_client = ScopedLeaderboard()

        self.design_getter = GetPlayoffDesign(original)
        self.design_getter_cloned = GetPlayoffDesign(to_clone)
        self.data_getter = GetPlayoffData(original)
        self.data_getter_cloned = GetPlayoffData(to_clone)

    def test_migrate_leaderboards_design(self):
        leaderboards = self.design_getter.get_leaderboards_design()
        leaderboards_count = len(leaderboards)

        self.scoped_client.migrate_leaderboards_design()

        leaderboards_cloned = self.design_getter_cloned.get_leaderboards_design()
        leaderboards_count_cloned = len(leaderboards_cloned)

        self.assertEqual(leaderboards_count, leaderboards_count_cloned)

        for board in leaderboards_cloned:
            leaderboard_design = self.design_getter_cloned\
                .get_single_leaderboard_design(board['id'])
            self.assertEqual(leaderboard_design['scope'], {"type": "custom"})

    def test_migrate_player_feed(self):
        # PRE
        # i due player sono appena stati creati e non hanno ancora nessun
        # feed

        player_id = "agazzani"
        player_aggr_id = "community_player_aggregate"

        player_feed = self.data_getter.get_player_feed(player_id)
        player_aggr_feed = self.data_getter.get_player_feed(player_aggr_id)

        self.scoped_client.migrate_player_feed({"player_id": player_id},
                                               player_feed)
        self.scoped_client.migrate_player_feed({"player_id": player_aggr_id},
                                               player_aggr_feed)

        player_feed = self.data_getter_cloned.get_player_feed(player_id)
        player_aggr_feed = self.data_getter_cloned\
            .get_player_feed(player_aggr_id)

        for feed in player_feed:
            if feed['event'] == 'action':
                player_scopes = feed['scopes']
                action_id = feed['action']['id']

                globale_scopes = ScopedUtility.get_globale_scopes(player_id,
                                                                  action_id)

                self.assertEqual(player_scopes, globale_scopes)

        for feed in player_aggr_feed:
            if feed['event'] == 'action':
                player_scopes = feed['scopes']

                lab_somma_scopes = ScopedUtility.get_lab_somma_scopes(player_aggr_id)

                self.assertEqual(player_scopes, lab_somma_scopes)
