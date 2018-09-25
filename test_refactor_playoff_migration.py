import unittest
from pprint import pprint

from refactor_playoff_migration import *

from playoff import Playoff, PlayoffException
from dotenv import load_dotenv


class UtilityTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_pagination(self):
        self.assertRaises(ParameterException, Utility.get_number_pages, -1)
        self.assertEqual(Utility.get_number_pages(0), 0)
        self.assertEqual(Utility.get_number_pages(1), 1)
        self.assertEqual(Utility.get_number_pages(100), 1)
        self.assertEqual(Utility.get_number_pages(101), 2)

    def test_raise_exception(self):
        self.assertRaises(ParameterException,
                          Utility.raise_empty_parameter_exception, [""])
        self.assertRaises(ParameterException,
                          Utility.raise_empty_parameter_exception, [{}])
        self.assertRaises(ParameterException,
                          Utility.raise_empty_parameter_exception, [[]])

    def test_playoff_client_factory(self):
        client_id = "GAMELABNOTARGETV01_CLIENT_ID"
        client_secret = "GAMELABNOTARGETV01_CLIENT_SECRET"

        client = Utility.get_playoff_client(client_id, client_secret)

        self.assertTrue(isinstance(client, Playoff))


class GetPlayoffDesignTest(unittest.TestCase):

    def setUp(self):
        playoff_client = Utility.get_playoff_client(
            "GAMELABNOTARGETV01_CLIENT_ID",
            "GAMELABNOTARGETV01_CLIENT_SECRET"
        )

        self.design_getter = GetPlayoffDesign(playoff_client)

    def test_get_design_methods(self):
        teams_design = self.design_getter.get_teams_design()
        metrics_design = self.design_getter.get_metrics_design()
        actions_design = self.design_getter.get_actions_design()
        leaderboards_design = self.design_getter.get_leaderboards_design()

        self.assertTrue(isinstance(teams_design, list))
        self.assertTrue(isinstance(metrics_design, list))
        self.assertTrue(isinstance(actions_design, list))
        self.assertTrue(isinstance(leaderboards_design, list))

    def test_get_singles_design(self):
        team_id = "globale"
        metric_id = "punti"
        action_id = "sfida_circle_the_dot"
        leaderboard_id = "globale_punti"

        team_result = self.design_getter.get_single_team_design(team_id)
        metric_result = self.design_getter.get_single_metric_design(metric_id)
        action_result = self.design_getter.get_single_action_design(action_id)
        leaderboard_result = self.design_getter.get_single_leaderboard_design(
            leaderboard_id)

        self.assertTrue(isinstance(team_result, dict))
        self.assertTrue(isinstance(metric_result, dict))
        self.assertTrue(isinstance(action_result, dict))
        self.assertTrue(isinstance(leaderboard_result, dict))

        self.assertEqual(team_result['id'], team_id)
        self.assertEqual(metric_result['id'], metric_id)
        self.assertEqual(action_result['id'], action_id)
        self.assertEqual(leaderboard_result['id'], leaderboard_id)


class PostDeletePlayoffDesignTest(unittest.TestCase):

    def setUp(self):
        playoff_client = Utility.get_playoff_client(
            "GAMELABCLONSCOPED2_CLIENT_ID",
            "GAMELABCLONSCOPED2_CLIENT_SECRET"
        )

        self.design_poster = PostPlayoffDesign(playoff_client)
        self.design_getter = GetPlayoffDesign(playoff_client)
        self.design_deleter = DeletePlayoffDesign(playoff_client)

    def test_create_team_design(self):
        team_id = "base_team"

        self.assertRaises(PlayoffException,
                          self.design_getter.get_single_team_design, team_id)

        valid_data = {
            'name': 'Base Team',
            'id': team_id,
            'permissions': [[
                'Giocatore',
                {
                    'assign': True,
                    'leave': True,
                    'lock': True,
                    'peer': True
                }
            ]],
            'creator_roles': ['Giocatore'],
            'settings': {
                'access': ['PUBLIC'],
                'max_global_instances': 'Infinity',
                'max_player_instances': 'Infinity',
                'max_players': 'Infinity',
                'public': True,
                'requires': {}
            },
            '_hues': {'Giocatore': 85}
        }

        teams_design = self.design_getter.get_teams_design()
        old_count = len(teams_design)

        self.design_poster.create_team_design(valid_data)

        teams_design = self.design_getter.get_teams_design()
        new_count = len(teams_design)

        self.assertEqual(new_count, old_count + 1)

        self.design_deleter.delete_single_team_design(team_id)

        teams_design = self.design_getter.get_teams_design()
        new_count = len(teams_design)

        self.assertEqual(new_count, old_count)

        self.assertRaises(PlayoffException,
                          self.design_deleter.delete_single_team_design,
                          team_id)

    def test_create_metric_design(self):
        metric_id = "ep"

        self.assertRaises(PlayoffException,
                          self.design_getter.get_single_metric_design,
                          metric_id)

        valid_data = {
            "id": metric_id,
            "name": "Experience Points",
            "type": "point",
            "constraints": {
                "min": "0",
                "max": "Infinity",
                "default": "0"
            }
        }

        metrics_design = self.design_getter.get_metrics_design()
        old_count = len(metrics_design)

        self.design_poster.create_metric_design(valid_data)

        metrics_design = self.design_getter.get_metrics_design()
        new_count = len(metrics_design)

        self.assertEqual(new_count, old_count + 1)

        self.design_deleter.delete_single_metric_design(metric_id)

        metrics_design = self.design_getter.get_metrics_design()
        new_count = len(metrics_design)

        self.assertEqual(new_count, old_count)

        self.assertRaises(PlayoffException,
                          self.design_deleter.delete_single_metric_design,
                          metric_id)

    def test_create_action_design(self):
        metric_data = {
            "id": "ep",
            "name": "Experience Points",
            "type": "point",
            "constraints": {
                "min": "0",
                "max": "Infinity",
                "default": "0"
            }
        }

        self.design_poster.create_metric_design(metric_data)

        action_id = "sfida1"

        self.assertRaises(PlayoffException,
                          self.design_getter.get_single_action_design,
                          action_id)

        valid_data = {
            "id": action_id,
            "name": "Sfida 1",
            "requires": {},
            "rules": [
                {
                    "requires": {},
                    "rewards": [
                        {
                            "metric": {
                                "id": "experience_point",
                                "type": "point"
                            },
                            "verb": "add",
                            "value": "5"
                        }
                    ]
                }
            ],
            "variables": []
        }

        actions_design = self.design_getter.get_actions_design()
        old_count = len(actions_design)

        self.design_poster.create_action_design(valid_data)

        actions_design = self.design_getter.get_actions_design()
        new_count = len(actions_design)

        self.assertEqual(new_count, old_count + 1)

        self.design_deleter.delete_single_metric_design("ep")
        self.design_deleter.delete_single_action_design(action_id)

        actions_design = self.design_getter.get_actions_design()
        new_count = len(actions_design)

        self.assertEqual(new_count, old_count)

        self.assertRaises(PlayoffException,
                          self.design_deleter.delete_single_action_design,
                          action_id)

    def test_create_leaderboard_design(self):
        metric_data = {
            "id": "ep",
            "name": "Experience Points",
            "type": "point",
            "constraints": {
                "min": "0",
                "max": "Infinity",
                "default": "0"
            }
        }

        self.design_poster.create_metric_design(metric_data)

        leaderboard_id = "all_time"

        self.assertRaises(PlayoffException,
                          self.design_getter.get_single_leaderboard_design,
                          leaderboard_id)

        valid_data = {
            "id": leaderboard_id,
            "name": "All Time",
            "entity_type": "players",
            "scope": {
                "type": "game"
            },
            "metric": {
                "id": "ep",
                "type": "point"
            }
        }

        leaderboards_design = self.design_getter.get_leaderboards_design()
        old_count = len(leaderboards_design)

        self.design_poster.create_leaderboard_design(valid_data)

        leaderboards_design = self.design_getter.get_leaderboards_design()
        new_count = len(leaderboards_design)

        self.assertEqual(new_count, old_count + 1)

        self.design_deleter.delete_single_metric_design("ep")
        self.design_deleter.delete_single_leaderboard_design(leaderboard_id)

        leaderboards_design = self.design_getter.get_leaderboards_design()
        new_count = len(leaderboards_design)

        self.assertEqual(new_count, old_count)

        self.assertRaises(PlayoffException,
                          self.design_deleter.delete_single_leaderboard_design,
                          leaderboard_id)


class GetPlayoffDataTest(unittest.TestCase):

    def setUp(self):
        playoff_client = Utility.get_playoff_client(
            "GAMELABNOTARGETV01_CLIENT_ID",
            "GAMELABNOTARGETV01_CLIENT_SECRET"
        )

        self.data_getter = GetPlayoffData(playoff_client)

    def test_count_method(self):
        team_id = "globale"

        team_instances_count = self.data_getter.get_team_count()
        players_count = self.data_getter.get_players_count()
        players_count_team = self.data_getter.get_players_count_in_team(team_id)

        self.assertTrue(isinstance(team_instances_count, int))
        self.assertTrue(isinstance(players_count, int))
        self.assertTrue(isinstance(players_count_team, int))
        self.assertTrue(team_instances_count >= 0)
        self.assertTrue(players_count >= 0)
        self.assertTrue(players_count_team >= 0)

    def test_info_by_id(self):
        teams_by_id = self.data_getter.get_teams_by_id()
        players_by_id = self.data_getter.get_players_by_id()
        game_id = self.data_getter.get_game_id()

        self.assertTrue(isinstance(teams_by_id, list))
        self.assertTrue(isinstance(players_by_id, list))
        self.assertTrue(isinstance(game_id, str))

    def test_team_info(self):
        team_id = "globale"
        team_info_keys = ['id', 'name', 'definition', 'roles']

        team_info = self.data_getter.get_team_info(team_id)

        self.assertTrue(isinstance(team_info, dict))

        for key in team_info_keys:
            self.assertTrue(key in team_info.keys())

    def test_player_profile(self):
        player_id = "agazzani"
        player_info_keys = ['alias', 'id', 'teams']

        player_info = self.data_getter.get_player_profile(player_id)

        self.assertTrue(isinstance(player_info, dict))

        for key in player_info_keys:
            self.assertTrue(key in player_info.keys())

    def test_player_feed(self):
        player1 = "agazzani"
        player2 = "utente01"  # player with no feed
        player_feed_keys = ["event", "id", "timestamp"]

        player1_feed = self.data_getter.get_player_feed(player1)
        player2_feed = self.data_getter.get_player_feed(player2)

        self.assertTrue(isinstance(player1_feed, list))
        self.assertTrue(isinstance(player2_feed, list))

        for feed in player1_feed:
            for key in player_feed_keys:
                self.assertTrue(key in feed.keys())

    def test_leaderboard(self):
        leaderboard_id = "globale_punti"
        leaderboard_keys = ["data", "total"]

        leaderboard_data = self.data_getter.get_leaderboard(leaderboard_id)

        self.assertTrue(isinstance(leaderboard_data, dict))

        for key in leaderboard_keys:
            self.assertTrue(key in leaderboard_data.keys())


class PostDeletePlayoffDataTest(unittest.TestCase):

    def setUp(self):
        playoff_client = Utility.get_playoff_client(
            "GAMELABCLONSCOPED2_CLIENT_ID",
            "GAMELABCLONSCOPED2_CLIENT_SECRET"
        )

        self.data_deleter = DeletePlayoffData(playoff_client)
        self.data_poster = PostPlayoffData(playoff_client)
        self.data_getter = GetPlayoffData(playoff_client)

    def test_create_team(self):
        # this team design must exists in the game
        existing_team_design = "globale"

        team_id = "test_team"

        valid_data = {
            "id": team_id,
            "name": "TestTeam",
            "access": "PUBLIC",
            "definition": existing_team_design
        }

        self.assertRaises(PlayoffException, self.data_getter.get_team_info,
                          team_id)

        old_count = self.data_getter.get_team_count()

        self.data_poster.create_team(valid_data)

        new_count = self.data_getter.get_team_count()

        self.assertEqual(old_count, new_count - 1)

        team_data = self.data_getter.get_team_info(team_id)

        self.assertEqual(team_data["id"], team_id)

        self.data_deleter.delete_single_team(team_id)

        new_count = self.data_getter.get_team_count()

        self.assertRaises(PlayoffException, self.data_getter.get_team_info,
                          team_id)
        self.assertEqual(old_count, new_count)

    def test_create_player(self):
        player_id = "player_nuovo"

        self.assertRaises(PlayoffException,
                          self.data_getter.get_player_profile, player_id)

        player_data = {
            "id": player_id,
            "alias": "Player Nuovo"
        }

        old_count = self.data_getter.get_players_count()

        self.data_poster.create_player(player_data)

        new_count = self.data_getter.get_players_count()

        self.assertEqual(old_count, new_count - 1)

        self.data_deleter.delete_single_player(player_id)

        new_count = self.data_getter.get_players_count()

        self.assertEqual(old_count, new_count)

        self.assertRaises(PlayoffException,
                          self.data_getter.get_player_profile, player_id)

    def test_join_team(self):
        player_id = "player_nuovo"
        team_id = "globale"

        player_data = {
            "id": player_id,
            "alias": "Player Nuovo"
        }

        self.data_poster.create_player(player_data)

        player_profile = self.data_getter.get_player_profile(player_id)

        self.assertTrue(not player_profile["teams"])

        valid_data = {
                "requested_roles": {
                    "Giocatore": True
                },
                "player_id": player_id
            }

        old_count = self.data_getter.get_players_count_in_team(team_id)

        self.data_poster.join_team(team_id, valid_data)

        new_count = self.data_getter.get_players_count_in_team(team_id)

        self.assertEqual(old_count, new_count - 1)

        self.data_deleter.delete_single_player(player_id)

        new_count = self.data_getter.get_players_count_in_team(team_id)

        self.assertEqual(old_count, new_count)

    def test_take_an_action(self):
        # this action design must exists in the game
        action_id = "sfida_circle_the_dot"

        player_id = "player_nuovo"

        player_data = {
            "id": player_id,
            "alias": "Player Nuovo"
        }

        self.data_poster.create_player(player_data)

        valid_data = {
            "variables": {
                'livello': 0,
                'punteggio': 100,
                'punteggioMedio': 100,
                'tentativi': 1
            },
            "scopes": []
        }

        player_feed = self.data_getter.get_player_feed(player_id)

        old_count = len(player_feed)

        self.data_poster.take_action(action_id, {"player_id": player_id},
                                     valid_data)

        player_feed = self.data_getter.get_player_feed(player_id)

        new_count = len(player_feed)

        self.assertEqual(old_count, new_count - 1)

        self.data_deleter.delete_single_player(player_id)


class MigrationDataTest(unittest.TestCase):

    def setUp(self):
        to_clone = Utility.get_playoff_client(
            "GAMELABCLONSCOPED2_CLIENT_ID",
            "GAMELABCLONSCOPED2_CLIENT_SECRET"
        )

        self.migrate_data = PlayoffMigrationData()
        self.data_getter_cloned = GetPlayoffData(to_clone)

    def test1_teams_migration(self):
        origin_teams_id = self.migrate_data.data_getter.get_teams_by_id()

        self.migrate_data.migrate_teams()

        cloned_teams_id = self.data_getter_cloned.get_teams_by_id()

        self.assertEqual(len(origin_teams_id), len(cloned_teams_id))
        self.assertEqual(origin_teams_id, cloned_teams_id)

    def test2_players_migration(self):
        self.migrate_data.data_destroyer.delete_players()

        origin_players_id = self.migrate_data.data_getter.get_players_by_id()

        for player in origin_players_id:
            player_data = self.migrate_data.data_getter.get_player_profile(
                player)

            player_feed = self.migrate_data.data_getter.get_player_feed(player)
            player_id = {"player_id": player}

            self.migrate_data.migrate_player_data(player_data)

            cloned_players_id = self.data_getter_cloned.get_players_by_id()

            self.assertTrue(player in cloned_players_id)

            origin_player_teams = player_data['teams']

            self.migrate_data.migrate_player_in_teams(player_data)

            cloned_player_data = self.data_getter_cloned.get_player_profile(
                player)
            cloned_player_teams = cloned_player_data['teams']

            self.assertEqual(origin_player_teams, cloned_player_teams)

            self.migrate_data.migrate_player_feed(player_id, player_feed)

            """
            Problema nel testare i feed clonati
            1) non posso controllare il numero in quanto prendo solo i feed con
                campo ['event'] == 'action'
            2) non posso controllare che le feed siano le stesse in quanto 
                l'ordine non è lo stesso
            3) non riesco a controllare i punteggi, in quanto alcuni
            
            cloned_player_data = self.data_getter_cloned.get_player_profile(
                player)
            self.assertEqual(player_data['scores'], 
                             cloned_player_data['scores'])
            """

        cloned_players_id = self.data_getter_cloned.get_players_by_id()

        self.assertEqual(origin_players_id, cloned_players_id)


class MigrationDesignTest(unittest.TestCase):

    def setUp(self):
        to_clone = Utility.get_playoff_client(
            "GAMELABCLONSCOPED2_CLIENT_ID",
            "GAMELABCLONSCOPED2_CLIENT_SECRET"
        )

        self.migrate_design = PlayoffMigrationDesign()
        self.design_getter = GetPlayoffDesign(to_clone)

    def test1_teams_design_migration(self):
        origin_teams_de = self.migrate_design.design_getter.get_teams_design()

        self.migrate_design.migrate_teams_design()

        clone_teams_de = self.design_getter.get_teams_design()

        self.assertEqual(origin_teams_de, clone_teams_de)

        for origin_design_data in origin_teams_de:
            design_id = origin_design_data['id']

            origin_design = self.migrate_design.design_getter\
                .get_single_team_design(design_id)

            cloned_design = self.design_getter.get_single_team_design(
                design_id)

            self.assertEqual(origin_design, cloned_design)

    def test2_metrics_design_migration(self):
        origin_metrics_des = self.migrate_design.design_getter\
            .get_metrics_design()

        self.migrate_design.migrate_metrics_design()

        clone_metrics_des = self.design_getter.get_metrics_design()

        self.assertEqual(origin_metrics_des, clone_metrics_des)

        for origin_metric_data in origin_metrics_des:
            design_id = origin_metric_data['id']

            origin_design = self.migrate_design.design_getter\
                .get_single_metric_design(design_id)

            cloned_design = self.design_getter.get_single_metric_design(
                design_id)

            self.assertEqual(origin_design, cloned_design)

    def test3_actions_design_migration(self):
        self.migrate_design.migrate_metrics_design()

        origin_action_des = self.migrate_design.design_getter\
            .get_actions_design()

        self.migrate_design.migrate_actions_design()

        clone_action_des = self.design_getter.get_actions_design()

        self.assertEqual(origin_action_des, clone_action_des)

        for origin_action_data in origin_action_des:
            action_id = origin_action_data['id']

            origin_design = self.migrate_design.design_getter\
                .get_single_action_design(action_id)

            cloned_design = self.design_getter.get_single_action_design(
                action_id)

            self.assertEqual(origin_design, cloned_design)

    def test4_leaderboards_design_migration(self):
        self.migrate_design.migrate_metrics_design()

        origin_boards_des = self.migrate_design.design_getter\
            .get_leaderboards_design()

        self.migrate_design.migrate_leaderboards_design()

        clone_boards_des = self.design_getter.get_leaderboards_design()

        self.assertEqual(origin_boards_des, clone_boards_des)

        for origin_boards_data in origin_boards_des:
            board_id = origin_boards_data['id']

            origin_design = self.migrate_design.design_getter\
                .get_single_leaderboard_design(board_id)

            cloned_design = self.design_getter\
                .get_single_leaderboard_design(board_id)

            self.assertEqual(origin_design, cloned_design)
