import os
from pprint import pprint

from playoff import Playoff
from dotenv import load_dotenv

# =======================
# EXCEPTION CLASS
# =======================


class ParameterException(Exception):
    """Class that define an exception for parameters methods"""
    pass

# =======================
# CONVENIENT CLASS
# =======================


class Constant(object):
    """Class that define some useful costant"""

    VERSION = "latest"
    TOTAL = "total"
    PLAYER_ID = "atomasse"
    BIG_NUMBER = 10 ** 10
    CYCLE = "alltime"

    ADMIN_ROOT = "/admin/"
    ADMIN_PLAYERS = "/admin/players/"
    ADMIN_TEAMS = "/admin/teams/"

    DESIGN_TEAMS = "/design/versions/" + VERSION + "/teams/"
    DESIGN_ACTIONS = "/design/versions/" + VERSION + "/actions/"
    DESIGN_METRICS = "/design/versions/" + VERSION + "/metrics/"
    DESIGN_LEADERBOARDS = "/design/versions/" + VERSION + "/leaderboards/"

    RUNTIME_ACTION = "/runtime/actions/"
    RUNTIME_LEADERBOARDS = "/runtime/leaderboards/"


class Utility(object):
    """Class that define some useful methods"""

    @staticmethod
    def get_number_pages(number):
        """Return number of pages

        :param number: number of items to paginate
        :raise ParameterException: if parameter is negative

        Pages refers to pagination
        Every page has 100 item, so:
        number = 100 -> return 1
        number = 101 -> return 2
        """
        if number < 0:
            raise ParameterException("Parameter can't be negative")

        division_res = int(number / 100)

        return division_res if number % 100 == 0 else division_res + 1

    @staticmethod
    def raise_empty_parameter_exception(parameters):
        for par in parameters:
            if not par:
                raise ParameterException("Parameter can't be empty")

    @staticmethod
    def get_playoff_client(client_id, client_secret):
        """Return Playoff game instance given his client id and client secret

        :param client_id: Playoff game client id
        :param client_secret: Playoff game client secret
        :return: Playoff game instance
        """
        Utility.raise_empty_parameter_exception([client_id, client_secret])

        from pathlib import Path
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)

        return Playoff(
            client_id=os.environ[client_id],
            client_secret=os.environ[client_secret],
            type='client',
            allow_unsecure=True
        )


# =======================
# DESIGN MANIPULATION CLASS
# =======================


class GetPlayoffDesign(object):
    """Class that make GET call via Playoff client to retrieve design from
    the Playoff game
    """

    def __init__(self, game: Playoff):
        self.game = game

    def get_teams_design(self):
        """Return a list containing all teams design"""
        return self.game.get(Constant.DESIGN_TEAMS, {})

    def get_single_team_design(self, team_id):
        """Return design of the chosen team

        :param str team_id: id of the team
        """
        Utility.raise_empty_parameter_exception([team_id])

        return self.game.get(Constant.DESIGN_TEAMS + team_id, {})

    def get_metrics_design(self):
        """Return a list containing all metrics design"""
        return self.game.get(Constant.DESIGN_METRICS, {})

    def get_single_metric_design(self, metric_id):
        """Return design of the chosen metric

        :param str metric_id: id of metric
        """
        Utility.raise_empty_parameter_exception([metric_id])

        return self.game.get(Constant.DESIGN_METRICS + metric_id, {})

    def get_actions_design(self):
        """Return a list containing all actions design"""
        return self.game.get(Constant.DESIGN_ACTIONS, {})

    def get_single_action_design(self, action_id):
        """Return design of the chosen action

        :param str action_id: id of action
        """
        Utility.raise_empty_parameter_exception([action_id])

        return self.game.get(Constant.DESIGN_ACTIONS + action_id, {})

    def get_leaderboards_design(self):
        """Return a list of dict containing leaderboards design id and name"""
        return self.game.get(Constant.DESIGN_LEADERBOARDS, {})

    def get_single_leaderboard_design(self, leaderboard_id):
        """Return design of the chosen leaderboard

        :param str leaderboard_id: id of leaderboard
        """
        Utility.raise_empty_parameter_exception([leaderboard_id])

        return self.game.get(Constant.DESIGN_LEADERBOARDS + leaderboard_id, {})


class PostPlayoffDesign(object):
    """Class that make POST call via Playoff client to create design
    in the Playoff game
    """
    def __init__(self, game: Playoff):
        self.game = game

    def create_team_design(self, design_data):
        """Create a team design

        :param dict design_data: info necessary to create a team design
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([design_data])

        self.game.post(Constant.DESIGN_TEAMS, {}, design_data)

    def create_metric_design(self, design_data):
        """Create a metric design

        :param dict design_data: info necessary to create a metric design
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([design_data])

        self.game.post(Constant.DESIGN_METRICS, {}, design_data)

    def create_action_design(self, design_data):
        """Create a action design

        :param dict design_data: info necessary to create an action design
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([design_data])

        self.game.post(Constant.DESIGN_ACTIONS, {}, design_data)

    def create_leaderboard_design(self, design_data):
        """Create a leaderboard design

        :param dict design_data: info necessary to create an leaderboard design
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([design_data])

        self.game.post(Constant.DESIGN_LEADERBOARDS, {}, design_data)


class DeletePlayoffDesign(object):
    """Class that make DELETE call via Playoff client to erase design
    from the Playoff game
    """

    def __init__(self, game: Playoff):
        self.game = game
        self.design_getter = GetPlayoffDesign(game)

    def delete_single_team_design(self, team_id):
        """Delete chosen team_id from the game

        :param str team_id: team id to delete
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([team_id])

        self.game.delete(Constant.DESIGN_TEAMS + team_id, {})

    def delete_single_metric_design(self, metric_id):
        """Delete chosen team_id from the game

        :param str metric_id: team id to delete
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([metric_id])

        self.game.delete(Constant.DESIGN_METRICS + metric_id, {})

    def delete_single_action_design(self, action_id):
        """Delete chosen team_id from the game

        :param str action_id: team id to delete
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([action_id])

        self.game.delete(Constant.DESIGN_ACTIONS + action_id, {})

    def delete_single_leaderboard_design(self, leaderboard_id):
        """Delete chosen team_id from the game

        :param str leaderboard_id: team id to delete
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([leaderboard_id])

        self.game.delete(Constant.DESIGN_LEADERBOARDS + leaderboard_id, {})

    def delete_teams_design(self):
        """Delete teams design"""
        teams_design = self.design_getter.get_teams_design()

        for team in teams_design:
            self.delete_single_team_design(team['id'])

    def delete_metrics_design(self):
        """Delete metrics design"""
        metrics_design = self.design_getter.get_metrics_design()

        for metric in metrics_design:
            self.delete_single_metric_design(metric['id'])

    def delete_actions_design(self):
        """Delete actions design"""
        actions_design = self.design_getter.get_actions_design()

        for action in actions_design:
            self.delete_single_action_design(action['id'])

    def delete_leaderboards_design(self):
        """Delete leaderboards design"""
        leaderboards_design = self.design_getter.get_leaderboards_design()

        for leaderboard in leaderboards_design:
            self.delete_single_leaderboard_design(leaderboard['id'])

    def delete_all_design(self):
        """Delete all design from the game"""
        self.delete_leaderboards_design()
        self.delete_actions_design()
        self.delete_metrics_design()
        self.delete_teams_design()


# =======================
# DATA MANIPULATION CLASS
# =======================

class GetPlayoffData(object):
    """Class that make GET call via Playoff client to retrieve data from
    the Playoff game
    """

    def __init__(self, game: Playoff):
        self.game = game

    # ==============
    # COUNT METHODS
    # ==============

    def get_team_count(self):
        """Return number of teams in the game"""
        return self.game.get(Constant.ADMIN_TEAMS, {})[Constant.TOTAL]

    def get_players_count(self):
        """Returns number of players in the game"""
        return self.game.get(Constant.ADMIN_PLAYERS, {})[Constant.TOTAL]

    def get_players_count_in_team(self, team_id):
        """Return number of players of the chosen team

        :param str team_id: containing id of a team
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([team_id])

        return self.game.get(Constant.ADMIN_TEAMS + team_id +
                             '/members', {})[Constant.TOTAL]

    # ==============
    # INFO METHODS
    # ==============

    def get_game_id(self):
        """ Returns game id of the chosen game """
        return self.game.get(Constant.ADMIN_ROOT)["game"]["id"]

    def get_teams_by_id(self):
        """Returns a list of teams id"""
        teams_id = []
        number_teams = self.get_team_count()
        number_pages = Utility.get_number_pages(number_teams)

        for count in range(number_pages):

            teams = self.game.get(Constant.ADMIN_TEAMS,
                                  {"skip": str(count * 100), "limit": "100"})

            for team in teams['data']:
                teams_id.append(team['id'])

        return teams_id

    def get_team_info(self, team_id):
        """Return information of the chosen team

        :param str team_id: containing id of a team
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([team_id])

        return self.game.get(Constant.ADMIN_TEAMS + team_id, {})

    def get_players_by_id(self):
        """Return a list of players id"""
        players_id = []
        number_players = self.get_players_count()
        number_pages = Utility.get_number_pages(number_players)

        for count in range(number_pages):
            players = self.game.get(Constant.ADMIN_PLAYERS,
                                    {"skip": str(count * 100), "limit": "100"})

            for player in players['data']:
                players_id.append(player['id'])

        return players_id

    def get_player_profile(self, player_id):
        """Return profile data of the chosen player

        :param str player_id: containing id of a player
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([player_id])

        return self.game.get(Constant.ADMIN_PLAYERS + player_id, {})

    def get_player_feed(self, player_id):
        """Return a list of feed of the chosen player

        :param str player_id: player id
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([player_id])

        player_feed = self.game.get(Constant.ADMIN_PLAYERS + player_id +
                                    "/activity", {"start": "0"})

        if player_feed is None:
            return []

        return player_feed

    def get_leaderboard(self, leaderboard_id):
        """Return chosen leaderboard

        :param str leaderboard_id: chosen leaderboard
        :raise: ParameterException: when parameter is empty
        """
        Utility.raise_empty_parameter_exception([leaderboard_id])

        data = {
            "player_id": Constant.PLAYER_ID,
            "cycle": Constant.CYCLE,
            "limit": Constant.BIG_NUMBER
        }

        return self.game.get(Constant.RUNTIME_LEADERBOARDS + leaderboard_id,
                             data)


class PostPlayoffData(object):
    """Class that make POST call via Playoff client to create instances
    in the Playoff game
    """

    def __init__(self, game: Playoff):
        self.game = game

    def create_team(self, team_data):
        """Create a team

        :param dict team_data: team info necessary to create a team
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([team_data])

        self.game.post(Constant.ADMIN_TEAMS, {}, team_data)

    def create_player(self, player_data):
        """Create a player

        :param dict player_data: player info necessary to create a player
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([player_data])

        self.game.post(Constant.ADMIN_PLAYERS, {}, player_data)

    def join_team(self, team_id, data):
        """Join a team

        :param str team_id: team id to join
        :param dict data: data necessary to join a team
        :raise ParameterException: if a parameter is empty
        """
        Utility.raise_empty_parameter_exception([team_id, data])

        self.game.post(Constant.ADMIN_TEAMS + team_id + "/join", {}, data)

    def take_action(self, action_id, player_id, data):
        """Take an action

        :param str action_id: action id to take
        :param dict player_id: player id that take action
        :param dict data: data necessary to take action
        :raise ParameterException: if a parameter is empty
        """
        Utility.raise_empty_parameter_exception([action_id, player_id, data])

        self.game.post(Constant.RUNTIME_ACTION + action_id + "/play",
                       player_id, data)


class DeletePlayoffData(object):
    """Class that make DELETE call via Playoff client to erase data
    from the Playoff game
    """

    def __init__(self, game: Playoff):
        self.game = game
        self.data_getter = GetPlayoffData(game)

    def delete_single_team(self, team_id):
        """Delete chosen team

        :param str team_id: team id to destroy
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([team_id])

        self.game.delete(Constant.ADMIN_TEAMS + team_id, {})

    def delete_single_player(self, player_id):
        """Delete chosen player

        :param str player_id: player id to destroy
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([player_id])

        self.game.delete(Constant.ADMIN_PLAYERS + player_id, {})

    def delete_teams(self):
        """Delete all teams"""
        teams_by_id = self.data_getter.get_teams_by_id()

        for team in teams_by_id:
            self.delete_single_team(team)

    def delete_players(self):
        """Delete all players"""
        players_by_id = self.data_getter.get_players_by_id()

        for player in players_by_id:
            self.delete_single_player(player)

    def delete_all_data(self):
        """Delete all data from the game"""
        self.delete_players()
        self.delete_teams()


# =======================
# MIGRATION CLASS
# =======================

class PlayoffMigrationData(object):
    """Class that make a migration of data from a Playoff game to an other"""

    def __init__(self):
        original = Utility.get_playoff_client(
            "GAMELABNOTARGETV01_CLIENT_ID",
            "GAMELABNOTARGETV01_CLIENT_SECRET"
        )

        to_clone = Utility.get_playoff_client(
            "GAMELABCLONSCOPED2_CLIENT_ID",
            "GAMELABCLONSCOPED2_CLIENT_SECRET"
        )

        self.data_getter = GetPlayoffData(original)
        self.data_destroyer = DeletePlayoffData(to_clone)
        self.data_creator = PostPlayoffData(to_clone)

    def migrate_teams(self):
        """Migrate teams"""

        self.data_destroyer.delete_teams()

        teams_by_id = self.data_getter.get_teams_by_id()

        for team in teams_by_id:
            team_data = self.data_getter.get_team_info(team)

            creation_data = {
                "id": team_data["id"],
                "name": team_data["name"],
                "access": team_data["access"],
                "definition": team_data["definition"]["id"]
            }

            self.data_creator.create_team(creation_data)

    def migrate_player_data(self, player_data):
        """Migrate players profile data

        :param dict player_data: player profile data
        :raise ParameterException: if a parameter is empty
        """
        Utility.raise_empty_parameter_exception([player_data])

        creation_data = {
            "id": player_data["id"],
            "alias": player_data["alias"]
        }

        self.data_creator.create_player(creation_data)

    def migrate_player_in_teams(self, player_data):
        """Migrate player in teams

        :param dict player_data: player profile data
        :raise ParameterException: if a parameter is empty
        """
        Utility.raise_empty_parameter_exception([player_data])

        for team in player_data["teams"]:
            data = {
                "requested_roles": {},
                "player_id": player_data["id"]
            }

            for role in team['roles']:
                data['requested_roles'].update({role: True})

            self.data_creator.join_team(team["id"], data)

    def migrate_player_feed(self, player_id, player_feed):
        """Migrate player feed

        :param dict player_id: player id in dict format
        :param dict player_feed: player feed (can be empty)
        :raise ParameterException: if player_id is empty
        """
        Utility.raise_empty_parameter_exception([player_id])

        for feed in player_feed:
            if feed["event"] == "action":
                action_id = feed['action']['id']
                data = {
                    "variables": feed['action']['vars'],
                    "scopes": feed['scopes']
                }

                self.data_creator.take_action(action_id, player_id, data)

    def migrate_players(self):
        """Migrate players"""

        self.data_destroyer.delete_players()

        players_by_id = self.data_getter.get_players_by_id()

        for player in players_by_id:
            player_data = self.data_getter.get_player_profile(player)
            player_feed = self.data_getter.get_player_feed(player)
            player_id = {"player_id": player}

            self.migrate_player_data(player_data)
            self.migrate_player_in_teams(player_data)
            self.migrate_player_feed(player_id, player_feed)

    def migrate_all_data(self):
        """Migrate all data"""
        self.migrate_teams()
        self.migrate_players()


class PlayoffMigrationDesign(object):
    """Class that make a migration of design from a Playoff game to an other"""

    def __init__(self):
        original = Utility.get_playoff_client(
            "GAMELABNOTARGETV01_CLIENT_ID",
            "GAMELABNOTARGETV01_CLIENT_SECRET"
        )

        to_clone = Utility.get_playoff_client(
            "GAMELABCLONSCOPED2_CLIENT_ID",
            "GAMELABCLONSCOPED2_CLIENT_SECRET"
        )

        self.design_getter = GetPlayoffDesign(original)
        self.design_destroyer = DeletePlayoffDesign(to_clone)
        self.design_creator = PostPlayoffDesign(to_clone)

    def migrate_teams_design(self):
        """Migrate teams design"""
        teams_design = self.design_getter.get_teams_design()

        self.design_destroyer.delete_teams_design()

        for team in teams_design:
            design_team = self.design_getter.get_single_team_design(team['id'])

            team_data = {
                'name': design_team['name'],
                'id': design_team['id'],
                'permissions': design_team['permissions'],
                'creator_roles': design_team['creator_roles'],
                'settings': design_team['settings'],
                '_hues': design_team['_hues']
            }

            if 'description' in design_team.keys():
                team_data.update({'description': design_team['description']})

            self.design_creator.create_team_design(team_data)

    def migrate_metrics_design(self):
        """Migrate metrics design"""
        metrics_design = self.design_getter.get_metrics_design()

        self.design_destroyer.delete_metrics_design()

        for metric in metrics_design:
            design_metric = self.design_getter\
                .get_single_metric_design(metric['id'])

            metric_data = {
                "id": design_metric['id'],
                "name": design_metric['name'],
                "type": design_metric['type'],
                "constraints": design_metric['constraints']
            }

            if "description" in design_metric.keys():
                metric_data.update({"description":
                                    design_metric["description"]})

            self.design_creator.create_metric_design(metric_data)

    def migrate_actions_design(self):
        """Migrate actions design"""
        actions_design = self.design_getter.get_actions_design()

        self.design_destroyer.delete_actions_design()

        for action in actions_design:
            design_action = self.design_getter\
                .get_single_action_design(action['id'])

            action_data = {
                "id": design_action['id'],
                "name": design_action['name'],
                "requires": design_action['requires'],
                "rules": design_action['rules'],
                "variables": design_action['variables'],
                "image": design_action['image']
            }

            if "description" in design_action.keys():
                action_data.update({"description":
                                    design_action["description"]})

            self.design_creator.create_action_design(action_data)

    def migrate_leaderboards_design(self):
        """Migrate leaderboards design"""
        leaderboards_design = self.design_getter.get_leaderboards_design()

        self.design_destroyer.delete_leaderboards_design()

        for leaderboard in leaderboards_design:
            design_leaderboard = self.design_getter\
                .get_single_leaderboard_design(leaderboard['id'])

            leaderboard_data = {
                "id": design_leaderboard['id'],
                "name": design_leaderboard['name'],
                "entity_type": design_leaderboard['entity_type'],
                "scope": design_leaderboard['scope'],
                "metric": design_leaderboard['metric'],
                "cycles": design_leaderboard['cycles']
            }

            if "description" in design_leaderboard.keys():
                leaderboard_data.update({"description":
                                        design_leaderboard["description"]})

            self.design_creator.create_leaderboard_design(leaderboard_data)

    def migrate_all_design(self):
        """Migrate all design"""
        self.migrate_teams_design()
        self.migrate_metrics_design()
        self.migrate_actions_design()
        self.migrate_leaderboards_design()
