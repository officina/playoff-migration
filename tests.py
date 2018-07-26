import unittest
import os

from refactor_playoff_migration import Utility, ParameterException, \
    GetPlayoffData

from playoff import Playoff
from dotenv import load_dotenv


class UtilityTest(unittest.TestCase):

    ut: Utility

    def setUp(self):
        self.ut = Utility()

    def test_pagination(self):
        self.assertRaises(ParameterException, self.ut.get_number_pages, -1)
        self.assertEqual(self.ut.get_number_pages(0), 0)
        self.assertEqual(self.ut.get_number_pages(1), 1)
        self.assertEqual(self.ut.get_number_pages(100), 1)
        self.assertEqual(self.ut.get_number_pages(101), 2)


class GetPlayoffDataTest(unittest.TestCase):

    gp: GetPlayoffData
    team_id: str

    def setUp(self):
        from pathlib import Path
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)
        playoff_client = Playoff(
            client_id=os.environ["GAMELABNOTARGETV01_CLIENT_ID"],
            client_secret=os.environ["GAMELABNOTARGETV01_CLIENT_SECRET"],
            type='client',
            allow_unsecure=True
        )

        self.gp = GetPlayoffData(playoff_client)

    def test_count_method(self):
        team_id = "globale"

        team_instances_count = self.gp.get_team_count()
        players_count = self.gp.get_players_count()
        players_count_team = self.gp.get_players_count_in_team(team_id)

        self.assertTrue(isinstance(team_instances_count, int))
        self.assertTrue(isinstance(players_count, int))
        self.assertTrue(isinstance(players_count_team, int))
        self.assertTrue(team_instances_count >= 0)
        self.assertTrue(players_count >= 0)
        self.assertTrue(players_count_team >= 0)
        self.assertRaises(ParameterException,
                          self.gp.get_players_count_in_team, '')

    def test_info_by_id(self):
        teams_by_id = self.gp.get_teams_by_id()
        players_by_id = self.gp.get_players_by_id()
        game_id = self.gp.get_game_id()

        self.assertTrue(isinstance(teams_by_id, list))
        self.assertTrue(isinstance(players_by_id, list))
        self.assertTrue(isinstance(game_id, str))

    def test_team_info(self):
        team_id = "globale"
        team_info_keys = ['id', 'name', 'definition', 'roles']

        team_info = self.gp.get_team_info(team_id)

        self.assertRaises(ParameterException, self.gp.get_team_info, '')
        self.assertTrue(isinstance(team_info, dict))

        for key in team_info_keys:
            self.assertTrue(key in team_info.keys())

    def test_player_info(self):
        player_id = "agazzani"
        player_info_keys = ['alias', 'id', 'teams']

        player_info = self.gp.get_player_profile(player_id)

        self.assertRaises(ParameterException, self.gp.get_player_profile, '')
        self.assertTrue(isinstance(player_info, dict))

        for key in player_info_keys:
            self.assertTrue(key in player_info.keys())

    def test_player_feed(self):
        player1 = "agazzani"
        player2 = "utente01"  # player with no feed
        player_feed_keys = ["event", "id", "timestamp"]

        player1_feed = self.gp.get_player_feed(player1)
        player2_feed = self.gp.get_player_feed(player2)

        self.assertRaises(ParameterException, self.gp.get_player_feed, '')
        self.assertTrue(isinstance(player1_feed, list))
        self.assertTrue(isinstance(player2_feed, list))

        for feed in player1_feed:
            for key in player_feed_keys:
                self.assertTrue(key in feed.keys())
