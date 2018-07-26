import os

from playoff import Playoff
from dotenv import load_dotenv


class ParameterException(Exception):
    pass


class Constant(object):
    """Class that define some useful costant"""

    ADMIN_ROOT = "/admin/"
    ADMIN_PLAYERS = "/admin/players/"
    ADMIN_TEAMS = "/admin/teams/"
    RUNTIME_ACTION = "/runtime/actions/"
    TOTAL = "total"


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
class DeletePlayoffData(object):
    """Class that make DELETE call via Playoff client to erase data
    from the Playoff game
    """

    def __init__(self, game: Playoff):
        self.game = game
        self.data_getter = GetPlayoffData(game)

    def delete_teams(self):
        """Delete all teams"""
        teams_by_id = self.data_getter.get_teams_by_id()

        for team in teams_by_id:
            self.game.delete(Constant.ADMIN_TEAMS + team, {})

    def delete_players(self):
        """Delete all players"""
        players_by_id = self.data_getter.get_players_by_id()

        for player in players_by_id:
            self.game.delete(Constant.ADMIN_PLAYERS + player, {})


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


class GetPlayoffDesign(object):
    pass


class DeletePlayoffDesign(object):
    pass


class PostPlayoffDesign(object):
    pass


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
