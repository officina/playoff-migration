import os

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

    ADMIN_ROOT = "/admin/"
    ADMIN_PLAYERS = "/admin/players/"
    ADMIN_TEAMS = "/admin/teams/"

    DESIGN_TEAMS = "/design/versions/" + VERSION + "/teams/"
    DESIGN_ACTIONS = "/design/versions/" + VERSION + "/actions/"
    DESIGN_METRICS = "/design/versions/" + VERSION + "/metrics/"
    DESIGN_LEADERBOARDS = "/design/versions/" + VERSION + "/leaderboards/"

    RUNTIME_ACTION = "/runtime/actions/"


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


# =======================
# DESIGN MANIPULATION CLASS
# =======================


# TODO: make tests for this class
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
        return self.game.get(Constant.DESIGN_TEAMS + team_id, {})

    def get_metrics_design(self):
        """Return a list containing all metrics design"""
        return self.game.get(Constant.DESIGN_METRICS, {})

    def get_single_metric_design(self, metric_id):
        """Return design of the chosen metric

        :param str metric_id: id of metric
        """
        return self.game.get(Constant.DESIGN_METRICS + metric_id, {})

    def get_actions_design(self):
        """Return a list containing all actions design"""
        return self.game.get(Constant.DESIGN_ACTIONS, {})

    def get_single_action_design(self, action_id):
        """Return design of the chosen action

        :param str action_id: id of action
        """
        return self.game.get(Constant.DESIGN_ACTIONS + action_id, {})

    def get_leaderboards_design(self):
        """Return a list containing all leaderboards design"""
        return self.game.get(Constant.DESIGN_LEADERBOARDS, {})

    def get_single_leaderboard_design(self, leaderboard_id):
        """Return design of the chosen leaderboard

        :param str leaderboard_id: id of leaderboard
        """
        return self.game.get(Constant.DESIGN_LEADERBOARDS + leaderboard_id, {})


# TODO: make tests for this class
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
        if not design_data:
            raise ParameterException("Parameter can't be empty")

        self.game.post(Constant.DESIGN_TEAMS, {}, design_data)

    def create_metric_design(self, design_data):
        """Create a metric design

        :param dict design_data: info necessary to create a metric design
        :raise ParameterException: if parameter is empty
        """
        if not design_data:
            raise ParameterException("Parameter can't be empty")

        self.game.post(Constant.DESIGN_METRICS, {}, design_data)

    def create_action_design(self, design_data):
        """Create a action design

        :param dict design_data: info necessary to create an action design
        :raise ParameterException: if parameter is empty
        """
        if not design_data:
            raise ParameterException("Parameter can't be empty")

        self.game.post(Constant.DESIGN_ACTIONS, {}, design_data)

    def create_leaderboard_design(self, design_data):
        """Create a leaderboard design

        :param dict design_data: info necessary to create an leaderboard design
        :raise ParameterException: if parameter is empty
        """
        if not design_data:
            raise ParameterException("Parameter can't be empty")

        self.game.post(Constant.DESIGN_LEADERBOARDS, {}, design_data)


# TODO: make tests for this class
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
        if not team_id:
            raise ParameterException("Parameter can't be empty")

        self.game.delete(Constant.DESIGN_TEAMS + team_id, {})

    def delete_single_metric_design(self, metric_id):
        """Delete chosen team_id from the game

        :param str metric_id: team id to delete
        :raise ParameterException: if parameter is empty
        """
        if not metric_id:
            raise ParameterException("Parameter can't be empty")

        self.game.delete(Constant.DESIGN_TEAMS + metric_id, {})

    def delete_single_action_design(self, action_id):
        """Delete chosen team_id from the game

        :param str action_id: team id to delete
        :raise ParameterException: if parameter is empty
        """
        if not action_id:
            raise ParameterException("Parameter can't be empty")

        self.game.delete(Constant.DESIGN_TEAMS + action_id, {})

    def delete_single_leaderboard_design(self, leaderboard_id):
        """Delete chosen team_id from the game

        :param str leaderboard_id: team id to delete
        :raise ParameterException: if parameter is empty
        """
        if not leaderboard_id:
            raise ParameterException("Parameter can't be empty")

        self.game.delete(Constant.DESIGN_TEAMS + leaderboard_id, {})

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
        if not team_id:
            raise ParameterException("Parameter can't be empty")

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
        if not team_id:
            raise ParameterException("Parameter can't be empty")

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
        if not player_id:
            raise ParameterException("Parameter can't be empty")

        return self.game.get(Constant.ADMIN_PLAYERS + player_id, {})

    def get_player_feed(self, player_id):
        """Return a list of feed of the chosen player

        :param str player_id: player id
        :raise ParameterException: if parameter is empty
        """
        if not player_id:
            raise ParameterException("Parameter can't be empty")

        player_feed = self.game.get(Constant.ADMIN_PLAYERS + player_id +
                                    "/activity", {"start": "0"})

        if player_feed is None:
            return []

        return player_feed


# TODO: make tests for this class
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
        if not team_data:
            raise ParameterException("Parameter can't be empty")

        self.game.post(Constant.ADMIN_TEAMS, {}, team_data)

    def create_player(self, player_data):
        """Create a player

        :param dict player_data: player info necessary to create a player
        :raise ParameterException: if parameter is empty
        """
        if not player_data:
            raise ParameterException("Parameter can't be empty")

        self.game.post(Constant.ADMIN_PLAYERS, {}, player_data)

    def join_team(self, team_id, data):
        """Join a team

        :param str team_id: team id to join
        :param dict data: data necessary to join a team
        :raise ParameterException: if a parameter is empty
        """
        if not team_id or not data:
            raise ParameterException("Parameter can't be empty")

        self.game.post(Constant.ADMIN_TEAMS + team_id + "/join", {}, data)

    def take_action(self, action_id, player_id, data):
        """Take an action

        :param str action_id: action id to take
        :param dict player_id: player id that take action
        :param dict data: data necessary to take action
        :raise ParameterException: if a parameter is empty
        """
        if not action_id or not player_id or not data:
            raise ParameterException("Parameter can't be empty")

        self.game.post(Constant.RUNTIME_ACTION + action_id + "/play",
                       player_id, data)


# TODO: make tests for this class
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
        if not team_id:
            raise ParameterException("Parameter can't be empty")

        self.game.delete(Constant.ADMIN_TEAMS + team_id, {})

    def delete_single_player(self, player_id):
        """Delete chosen player

        :param str player_id: player id to destroy
        :raise ParameterException: if parameter is empty
        """
        if not player_id:
            raise ParameterException("Parameter can't be empty")

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


# =======================
# MIGRATION CLASS
# =======================


# TODO: make tests for this class
class PlayoffMigrationData(object):
    """Class that make a migration of data from a Playoff game to an other"""

    def __init__(self):
        from pathlib import Path
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)

        self.original = Playoff(
            client_id=os.environ["GAMELABNOTARGETV01_CLIENT_ID"],
            client_secret=os.environ["GAMELABNOTARGETV01_CLIENT_SECRET"],
            type='client',
            allow_unsecure=True
        )

        self.to_clone = Playoff(
            client_id=os.environ["GAMELABCLONSCOPED2_CLIENT_ID"],
            client_secret=os.environ["GAMELABCLONSCOPED2_CLIENT_SECRET"],
            type='client',
            allow_unsecure=True
        )

        self.data_getter = GetPlayoffData(self.original)
        self.data_destroyer = DeletePlayoffData(self.to_clone)
        self.data_creator = PostPlayoffData(self.to_clone)

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

    def migrate_player_data(self, player_data):
        """Migrate players profile data

        :param dict player_data: player profile data
        :raise ParameterException: if a parameter is empty
        """
        if not player_data:
            raise ParameterException("Parameter can't be empty")

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
        if not player_data:
            raise ParameterException("Parameter can't be empty")

        for team in player_data["teams"]:
            data = {
                "requested_roles": {
                    team['roles'][0]: True
                },
                "player_id": player_data["id"]
            }

            self.data_creator.join_team(team["id"], data)

    def migrate_player_feed(self, player_id, player_feed):
        """Migrate player feed

        :param dict player_id: player id in dict format
        :param dict player_feed: player feed
        :raise ParameterException: if a parameter is empty
        """
        if not player_id or not player_feed:
            raise ParameterException("Parameter can't be empty")

        for feed in player_feed:
            if feed["event"] == ["action"]:
                action_id = feed['action']['id']
                data = {
                    "variables": feed['action']['vars'],
                    "scopes": feed['scopes']
                }

                self.data_creator.take_action(action_id, player_id, data)


# TODO: make tests for this class
class PlayoffMigrationDesign(object):
    """Class that make a migration of design from a Playoff game to an other"""

    def __init__(self):
        from pathlib import Path
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)

        self.original = Playoff(
            client_id=os.environ["GAMELABNOTARGETV01_CLIENT_ID"],
            client_secret=os.environ["GAMELABNOTARGETV01_CLIENT_SECRET"],
            type='client',
            allow_unsecure=True
        )

        self.to_clone = Playoff(
            client_id=os.environ["GAMELABCLONSCOPED2_CLIENT_ID"],
            client_secret=os.environ["GAMELABCLONSCOPED2_CLIENT_SECRET"],
            type='client',
            allow_unsecure=True
        )

        self.design_getter = GetPlayoffDesign(self.original)
        self.design_destroyer = DeletePlayoffDesign(self.to_clone)
        self.design_creator = PostPlayoffDesign(self.to_clone)

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

            self.design_creator.create_team_design(team_data)

    def migrate_metrics_design(self):
        """Migrate metrics design"""
        metrics_design = self.design_getter.get_metrics_design()

        self.design_destroyer.delete_metrics_design()

        for metric in metrics_design:
            design_metric = self.design_getter\
                .get_single_metric_design(metric['id'])

            metric_data = {
                'name': design_metric['name'],
                'id': design_metric['id'],
                'permissions': design_metric['permissions'],
                'creator_roles': design_metric['creator_roles'],
                'settings': design_metric['settings'],
                '_hues': design_metric['_hues']
            }

            self.design_creator.create_metric_design(metric_data)

    def migrate_actions_design(self):
        """Migrate actions design"""
        actions_design = self.design_getter.get_actions_design()

        self.design_destroyer.delete_actions_design()

        for action in actions_design:
            design_action = self.design_getter\
                .get_single_action_design(action['id'])

            action_data = {
                'name': design_action['name'],
                'id': design_action['id'],
                'permissions': design_action['permissions'],
                'creator_roles': design_action['creator_roles'],
                'settings': design_action['settings'],
                '_hues': design_action['_hues']
            }

            self.design_creator.create_action_design(action_data)

    def migrate_leaderboards_design(self):
        """Migrate leaderboards design"""
        leaderboards_design = self.design_getter.get_leaderboards_design()

        self.design_destroyer.delete_leaderboards_design()

        for leaderboard in leaderboards_design:
            design_leaderboard = self.design_getter\
                .get_single_leaderboard_design(leaderboard['id'])

            leaderboard_data = {
                'name': design_leaderboard['name'],
                'id': design_leaderboard['id'],
                'permissions': design_leaderboard['permissions'],
                'creator_roles': design_leaderboard['creator_roles'],
                'settings': design_leaderboard['settings'],
                '_hues': design_leaderboard['_hues']
            }

            self.design_creator.create_team_design(leaderboard_data)
