import os
from pprint import pprint
from logging import Logger
import logging

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


class MigrationLogger:
    __instance: Logger = None

    @staticmethod
    def get_instance():
        if MigrationLogger.__instance is None:
            MigrationLogger()
        return MigrationLogger.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if MigrationLogger.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            MigrationLogger.__instance = logging.getLogger("migration_logger")
            MigrationLogger.__instance.setLevel(logging.DEBUG)
            ch = logging.FileHandler(filename="migration.logger", mode="w")
            ch.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s",
                "%m/%d/%Y %I:%M:%S %p")
            ch.setFormatter(formatter)
            MigrationLogger.__instance.addHandler(ch)


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
        logger = MigrationLogger.get_instance()
        logger.debug("get_number_pages called")

        if number < 0:
            raise ParameterException("Parameter can't be negative")

        division_res = int(number / 100)

        return division_res if number % 100 == 0 else division_res + 1

    @staticmethod
    def raise_empty_parameter_exception(parameters):
        logger = MigrationLogger.get_instance()

        for par in parameters:
            if not par:
                logger.warning("parameters: " + parameters)

                raise ParameterException("Parameter can't be empty")

    @staticmethod
    def get_playoff_client(client_id, client_secret):
        """Return Playoff game instance given his client id and client secret

        :param client_id: Playoff game client id
        :param client_secret: Playoff game client secret
        :return: Playoff game instance
        """
        Utility.raise_empty_parameter_exception([client_id, client_secret])

        logger = MigrationLogger.get_instance()
        logger.info("A new playoff client will be created...")

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
        self.logger = MigrationLogger.get_instance()

    def get_teams_design(self):
        """Return a list containing all teams design"""
        self.logger.debug("calling playoff for teams design")

        return self.game.get(Constant.DESIGN_TEAMS, {})

    def get_single_team_design(self, team_id):
        """Return design of the chosen team

        :param str team_id: id of the team
        """
        Utility.raise_empty_parameter_exception([team_id])

        self.logger.debug("returning " + team_id + " design")

        return self.game.get(Constant.DESIGN_TEAMS + team_id, {})

    def get_metrics_design(self):
        """Return a list containing all metrics design"""
        self.logger.debug("calling playoff for metrics design")

        return self.game.get(Constant.DESIGN_METRICS, {})

    def get_single_metric_design(self, metric_id):
        """Return design of the chosen metric

        :param str metric_id: id of metric
        """
        Utility.raise_empty_parameter_exception([metric_id])

        self.logger.debug("returning " + metric_id + " design")

        return self.game.get(Constant.DESIGN_METRICS + metric_id, {})

    def get_actions_design(self):
        """Return a list containing all actions design"""
        self.logger.debug("calling playoff for actions design")

        return self.game.get(Constant.DESIGN_ACTIONS, {})

    def get_single_action_design(self, action_id):
        """Return design of the chosen action

        :param str action_id: id of action
        """
        Utility.raise_empty_parameter_exception([action_id])

        self.logger.debug("returning " + action_id + " design")

        return self.game.get(Constant.DESIGN_ACTIONS + action_id, {})

    def get_leaderboards_design(self):
        """Return a list of dict containing leaderboards design id and name"""
        self.logger.debug("calling playoff for leaderboards design")

        return self.game.get(Constant.DESIGN_LEADERBOARDS, {})

    def get_single_leaderboard_design(self, leaderboard_id):
        """Return design of the chosen leaderboard

        :param str leaderboard_id: id of leaderboard
        """
        Utility.raise_empty_parameter_exception([leaderboard_id])

        self.logger.debug("returning " + leaderboard_id + " design")

        return self.game.get(Constant.DESIGN_LEADERBOARDS + leaderboard_id, {})


class PostPlayoffDesign(object):
    """Class that make POST call via Playoff client to create design
    in the Playoff game
    """
    def __init__(self, game: Playoff):
        self.game = game
        self.logger = MigrationLogger.get_instance()

    def create_team_design(self, design_data):
        """Create a team design

        :param dict design_data: info necessary to create a team design
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([design_data])

        self.logger.debug("creating team design")

        self.game.post(Constant.DESIGN_TEAMS, {}, design_data)

        self.logger.debug("team design created")

    def create_metric_design(self, design_data):
        """Create a metric design

        :param dict design_data: info necessary to create a metric design
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([design_data])

        self.logger.debug("creating metric design")

        self.game.post(Constant.DESIGN_METRICS, {}, design_data)

        self.logger.debug("team design created")

    def create_action_design(self, design_data):
        """Create a action design

        :param dict design_data: info necessary to create an action design
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([design_data])

        self.logger.debug("creating action design")

        self.game.post(Constant.DESIGN_ACTIONS, {}, design_data)

        self.logger.debug("action design created")

    def create_leaderboard_design(self, design_data):
        """Create a leaderboard design

        :param dict design_data: info necessary to create an leaderboard design
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([design_data])

        self.logger.debug("creating leaderboard design")

        self.game.post(Constant.DESIGN_LEADERBOARDS, {}, design_data)

        self.logger.debug("leaderboard design created")


class DeletePlayoffDesign(object):
    """Class that make DELETE call via Playoff client to erase design
    from the Playoff game
    """

    def __init__(self, game: Playoff):
        self.game = game
        self.design_getter = GetPlayoffDesign(game)
        self.logger = MigrationLogger.get_instance()

    def delete_single_team_design(self, team_id):
        """Delete chosen team_id from the game

        :param str team_id: team id to delete
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([team_id])

        self.logger.debug("deleting " + team_id + " design")

        self.game.delete(Constant.DESIGN_TEAMS + team_id, {})

    def delete_single_metric_design(self, metric_id):
        """Delete chosen team_id from the game

        :param str metric_id: team id to delete
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([metric_id])

        self.logger.debug("deleting " + metric_id + " design")

        self.game.delete(Constant.DESIGN_METRICS + metric_id, {})

    def delete_single_action_design(self, action_id):
        """Delete chosen team_id from the game

        :param str action_id: team id to delete
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([action_id])

        self.logger.debug("deleting " + action_id + " design")

        self.game.delete(Constant.DESIGN_ACTIONS + action_id, {})

    def delete_single_leaderboard_design(self, leaderboard_id):
        """Delete chosen team_id from the game

        :param str leaderboard_id: team id to delete
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([leaderboard_id])

        self.logger.debug("deleting " + leaderboard_id + " design")

        self.game.delete(Constant.DESIGN_LEADERBOARDS + leaderboard_id, {})

    def delete_teams_design(self):
        """Delete teams design"""
        teams_design = self.design_getter.get_teams_design()
        teams_count = str(len(teams_design))

        self.logger.info(teams_count + " teams design will be deleted")
        index = 0

        for team in teams_design:
            self.delete_single_team_design(team['id'])

            index += 1
            self.logger.debug("team " + index + " of " + teams_count +
                              " deleted")

        self.logger.info("teams deleted")

    def delete_metrics_design(self):
        """Delete metrics design"""
        metrics_design = self.design_getter.get_metrics_design()
        metrics_count = str(len(metrics_design))

        self.logger.info(metrics_count + " metrics design will be deleted")
        index = 0

        for metric in metrics_design:
            self.delete_single_metric_design(metric['id'])

            index += 1
            self.logger.debug("metric " + index + " of " + metrics_count +
                              " deleted")

        self.logger.info("metrics deleted")

    def delete_actions_design(self):
        """Delete actions design"""
        actions_design = self.design_getter.get_actions_design()
        actions_count = str(len(actions_design))

        self.logger.info(actions_count + " actions design will be deleted")
        index = 0

        for action in actions_design:
            self.delete_single_action_design(action['id'])

            index += 1
            self.logger.debug("action " + index + " of " + actions_count +
                              " deleted")

        self.logger.info("actions deleted")

    def delete_leaderboards_design(self):
        """Delete leaderboards design"""
        leaderboards_design = self.design_getter.get_leaderboards_design()
        leaderboards_count = str(len(leaderboards_design))

        self.logger.info(leaderboards_count + " leaderboards design will be "
                                              "deleted")
        index = 0

        for leaderboard in leaderboards_design:
            self.delete_single_leaderboard_design(leaderboard['id'])

            index += 1
            self.logger.debug("leaderboard " + index + " of " +
                              leaderboards_count + " deleted")

        self.logger.info("leaderboards deleted")

    def delete_all_design(self):
        """Delete all design from the game"""
        self.logger.info("deleting all design")

        self.delete_leaderboards_design()
        self.delete_actions_design()
        self.delete_metrics_design()
        self.delete_teams_design()

        self.logger.info("all design deleted")


# =======================
# DATA MANIPULATION CLASS
# =======================

class GetPlayoffData(object):
    """Class that make GET call via Playoff client to retrieve data from
    the Playoff game
    """

    def __init__(self, game: Playoff):
        self.game = game
        self.logger = MigrationLogger.get_instance()

    # ==============
    # COUNT METHODS
    # ==============

    def get_team_count(self):
        """Return number of teams in the game"""
        self.logger.debug("returning number of teams")

        return self.game.get(Constant.ADMIN_TEAMS, {})[Constant.TOTAL]

    def get_players_count(self):
        """Returns number of players in the game"""
        self.logger.debug("returning number of players")

        return self.game.get(Constant.ADMIN_PLAYERS, {})[Constant.TOTAL]

    def get_players_count_in_team(self, team_id):
        """Return number of players of the chosen team

        :param str team_id: containing id of a team
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([team_id])

        self.logger.debug("returning number of players in team: " + team_id)

        return self.game.get(Constant.ADMIN_TEAMS + team_id +
                             '/members', {})[Constant.TOTAL]

    # ==============
    # INFO METHODS
    # ==============

    def get_game_id(self):
        """ Returns game id of the chosen game """
        self.logger.debug("returning game_id")

        return self.game.get(Constant.ADMIN_ROOT)["game"]["id"]

    def get_teams_by_id(self):
        """Returns a list of teams id"""
        teams_id = []
        number_teams = self.get_team_count()
        number_pages = Utility.get_number_pages(number_teams)

        self.logger.info("preparing list of teams id")

        for count in range(number_pages):

            teams = self.game.get(Constant.ADMIN_TEAMS,
                                  {"skip": str(count * 100), "limit": "100"})

            for team in teams['data']:
                teams_id.append(team['id'])

                self.logger.debug(team['id'] + "added to list")

        self.logger.info("returning list of teams id")

        return teams_id

    def get_team_info(self, team_id):
        """Return information of the chosen team

        :param str team_id: containing id of a team
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([team_id])

        self.logger.debug("returning info of team: " + team_id)

        return self.game.get(Constant.ADMIN_TEAMS + team_id, {})

    def get_players_by_id(self):
        """Return a list of players id"""
        players_id = []
        number_players = self.get_players_count()
        number_pages = Utility.get_number_pages(number_players)

        self.logger.info("preparing list of players id")

        for count in range(number_pages):
            players = self.game.get(Constant.ADMIN_PLAYERS,
                                    {"skip": str(count * 100), "limit": "100"})

            for player in players['data']:
                players_id.append(player['id'])

                self.logger.debug(player['id'] + "added to list")

        self.logger.info("returning list of players id")

        return players_id

    def get_player_profile(self, player_id):
        """Return profile data of the chosen player

        :param str player_id: containing id of a player
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([player_id])

        self.logger.debug("returning info of player: " + player_id)

        return self.game.get(Constant.ADMIN_PLAYERS + player_id, {})

    def get_player_feed(self, player_id):
        """Return a list of feed of the chosen player

        :param str player_id: player id
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([player_id])

        self.logger.debug("returning feed of player: " + player_id)

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

        self.logger.debug("returning leaderboard: " + leaderboard_id)

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
        self.logger = MigrationLogger.get_instance()

    def create_team(self, team_data):
        """Create a team

        :param dict team_data: team info necessary to create a team
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([team_data])

        self.logger.debug("creating team " + team_data['id'])

        self.game.post(Constant.ADMIN_TEAMS, {}, team_data)

        self.logger.debug("team created")

    def create_player(self, player_data):
        """Create a player

        :param dict player_data: player info necessary to create a player
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([player_data])

        self.logger.debug("creating player " + player_data['id'])

        self.game.post(Constant.ADMIN_PLAYERS, {}, player_data)

        self.logger.debug("player created")

    def join_team(self, team_id, data):
        """Join a team

        :param str team_id: team id to join
        :param dict data: data necessary to join a team
        :raise ParameterException: if a parameter is empty
        """
        Utility.raise_empty_parameter_exception([team_id, data])

        self.logger.debug("join team " + team_id)

        self.game.post(Constant.ADMIN_TEAMS + team_id + "/join", {}, data)

        self.logger.debug("team joined")

    def take_action(self, action_id, player_id, data):
        """Take an action

        :param str action_id: action id to take
        :param dict player_id: player id that take action
        :param dict data: data necessary to take action
        :raise ParameterException: if a parameter is empty
        """
        Utility.raise_empty_parameter_exception([action_id, player_id, data])

        self.logger.debug("taking action " + action_id + " by " + player_id)

        self.game.post(Constant.RUNTIME_ACTION + action_id + "/play",
                       player_id, data)

        self.logger.debug("action taken")


class DeletePlayoffData(object):
    """Class that make DELETE call via Playoff client to erase data
    from the Playoff game
    """

    def __init__(self, game: Playoff):
        self.game = game
        self.data_getter = GetPlayoffData(game)
        self.logger = MigrationLogger.get_instance()

    def delete_single_team(self, team_id):
        """Delete chosen team

        :param str team_id: team id to destroy
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([team_id])

        self.logger.debug("team " + team_id + " will be deleted")

        self.game.delete(Constant.ADMIN_TEAMS + team_id, {})

        self.logger.debug("team deleted")

    def delete_single_player(self, player_id):
        """Delete chosen player

        :param str player_id: player id to destroy
        :raise ParameterException: if parameter is empty
        """
        Utility.raise_empty_parameter_exception([player_id])

        self.logger.debug("player " + player_id + " will be deleted")

        self.game.delete(Constant.ADMIN_PLAYERS + player_id, {})

        self.logger.debug("player deleted")

    def delete_teams(self):
        """Delete all teams"""
        teams_by_id = self.data_getter.get_teams_by_id()
        teams_count = str(len(teams_by_id))

        self.logger.info(teams_count + " teams will be deleted")
        index = 0

        for team in teams_by_id:
            self.delete_single_team(team)

            index += 1
            self.logger.debug("team " + index + " of " + teams_count +
                              " deleted")

        self.logger.info("teams deleted")

    def delete_players(self):
        """Delete all players"""
        players_by_id = self.data_getter.get_players_by_id()
        players_count = str(len(players_by_id))

        self.logger.info(players_count + " players will be deleted")
        index = 0

        for player in players_by_id:
            self.delete_single_player(player)

            index += 1
            self.logger.debug("player " + index + " of " + players_count +
                              " deleted")

        self.logger.info("players deleted")

    def delete_all_data(self):
        """Delete all data from the game"""
        self.logger.info("deleting data")

        self.delete_players()
        self.delete_teams()

        self.logger.info("data deleted")


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
        self.logger = MigrationLogger.get_instance()

    def migrate_teams(self):
        """Migrate teams"""
        self.logger.info("migrating teams")

        self.data_destroyer.delete_teams()

        teams_by_id = self.data_getter.get_teams_by_id()

        for team in teams_by_id:
            self.logger.debug("migrating team " + team)

            team_data = self.data_getter.get_team_info(team)

            creation_data = {
                "id": team_data["id"],
                "name": team_data["name"],
                "access": team_data["access"],
                "definition": team_data["definition"]["id"]
            }

            self.data_creator.create_team(creation_data)

        self.logger.info("teams migration finished")

    def migrate_player_data(self, player_data):
        """Migrate players profile data

        :param dict player_data: player profile data
        :raise ParameterException: if a parameter is empty
        """
        Utility.raise_empty_parameter_exception([player_data])

        self.logger.debug("migrate player data")

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

        self.logger.debug("migrate player in teams")

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

        self.logger.debug("migrate feed of player " + player_id['player_id'])

        for feed in player_feed:
            if feed["event"] == "action":
                action_id = feed['action']['id']
                data = {
                    "variables": feed['action']['vars'],
                    "scopes": feed['scopes']
                }

                self.data_creator.take_action(action_id, player_id, data)

        self.logger.debug("feed migration finished")

    def migrate_players(self):
        """Migrate players"""
        self.logger.info("migrating players")

        self.data_destroyer.delete_players()

        players_by_id = self.data_getter.get_players_by_id()

        for player in players_by_id:
            self.logger.debug("migrating player " + player)

            player_data = self.data_getter.get_player_profile(player)
            player_feed = self.data_getter.get_player_feed(player)
            player_id = {"player_id": player}

            self.migrate_player_data(player_data)
            self.migrate_player_in_teams(player_data)
            self.migrate_player_feed(player_id, player_feed)

        self.logger.info("players migration finished")

    def migrate_all_data(self):
        """Migrate all data"""
        self.logger.info("starting data migration")

        self.migrate_teams()
        self.migrate_players()

        self.logger.info("data migration finished")


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
        self.logger = MigrationLogger.get_instance()

    def migrate_teams_design(self):
        """Migrate teams design"""
        self.logger.info("migrating teams design")

        teams_design = self.design_getter.get_teams_design()

        self.design_destroyer.delete_teams_design()

        for team in teams_design:
            self.logger.debug("migrating team design " + team['id'])

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

        self.logger.info("teams design migration finished")

    def migrate_metrics_design(self):
        """Migrate metrics design"""
        self.logger.info("migrating metrics design")

        metrics_design = self.design_getter.get_metrics_design()

        self.design_destroyer.delete_metrics_design()

        for metric in metrics_design:
            self.logger.debug("migrating metric design " + metric['id'])

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

        self.logger.info("metrics design migration finished")

    def migrate_actions_design(self):
        """Migrate actions design"""
        self.logger.info("migrating actions design")

        actions_design = self.design_getter.get_actions_design()

        self.design_destroyer.delete_actions_design()

        for action in actions_design:
            self.logger.debug("migrating action design " + action['id'])

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

        self.logger.info("actions design migration finished")

    def migrate_leaderboards_design(self):
        """Migrate leaderboards design"""
        self.logger.info("migrating leaderboards design")

        leaderboards_design = self.design_getter.get_leaderboards_design()

        self.design_destroyer.delete_leaderboards_design()

        for leaderboard in leaderboards_design:
            self.logger.debug("migrating leaderboard design " +
                              leaderboard['id'])

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

        self.logger.info("leaderboards design migration finished")

    def migrate_all_design(self):
        """Migrate all design"""
        self.logger.info("starting design migration")

        self.migrate_teams_design()
        self.migrate_metrics_design()
        self.migrate_actions_design()
        self.migrate_leaderboards_design()

        self.logger.info("design migration finished")
