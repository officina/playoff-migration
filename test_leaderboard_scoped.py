import unittest

from playoff_migration import *
from leaderboard_scoped import *


class ScopedLeaderboardTest(unittest.TestCase):

    def setUp(self):
        original = Utility.get_playoff_client(
            "ORIGINAL_CLIENT_ID",
            "ORIGINAL_CLIENT_SECRET"
        )

        to_clone = Utility.get_playoff_client(
            "CLONED_CLIENT_ID",
            "CLONED_CLIENT_SECRET"
        )

        self.scoped_client = ScopedLeaderboard()

        self.design_getter = GetPlayoffDesign(original)
        self.design_getter_cloned = GetPlayoffDesign(to_clone)
        self.data_getter = GetPlayoffData(original)
        self.data_getter_cloned = GetPlayoffData(to_clone)
        self.data_deleter_cloned = DeletePlayoffData(to_clone)
        self.data_poster_cloned = PostPlayoffData(to_clone)

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
        player_id = "agazzani"
        player_aggr_id = "community_player_aggregate"

        # Delete players
        self.data_deleter_cloned.delete_single_player(player_id)
        self.data_deleter_cloned.delete_single_player(player_aggr_id)

        # Create players
        player_data = {
            "id": player_id,
            "alias": player_id
        }
        player_aggr_data = {
            "id": player_aggr_id,
            "alias": player_aggr_id
        }

        self.data_poster_cloned.create_player(player_data)
        self.data_poster_cloned.create_player(player_aggr_data)

        # Add players to team
        player_profile = self.data_getter.get_player_profile(player_id)
        player_aggr_profile = self.data_getter.get_player_profile(
            player_aggr_id)

        for team in player_profile["teams"]:
            data = {
                "requested_roles": {
                    team['roles'][0]: True
                },
                "player_id": player_profile["id"]
            }

            self.data_poster_cloned.join_team(team["id"], data)

        for team in player_aggr_profile["teams"]:
            data = {
                "requested_roles": {
                    team['roles'][0]: True
                },
                "player_id": player_aggr_profile["id"]
            }

            self.data_poster_cloned.join_team(team["id"], data)

        # Actual test
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

                lab_somma_scopes = ScopedUtility.get_lab_somma_scopes(
                    player_aggr_id)

                self.assertEqual(player_scopes, lab_somma_scopes)
