from playoff import Playoff, PlayoffException
import os
from dotenv import load_dotenv
from pprint import pprint
from enum import Enum


class Games(Enum):
    """ Enumeration type that identifies each different game """
    original = "original"
    cloned = "cloned"


class PlayoffMigration(object):
    """ this class implements all the necessary methods and attributes to clone a game and scope its assetts in a
    second one """
    _original: Playoff = None
    _cloned: Playoff = None

    def __init__(self):
        from pathlib import Path  # python3 only
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)
        self._original = Playoff(
            client_id=os.environ["GAMELABNOTARGETV01_CLIENT_ID"],
            client_secret=os.environ["GAMELABNOTARGETV01_CLIENT_SECRET"],
            type='client',
            allow_unsecure=True
        )
        self._cloned = Playoff(
            client_id=os.environ["GAMELABCLONSCOPED_CLIENT_ID"],
            client_secret=os.environ["GAMELABCLONSCOPED_CLIENT_SECRET"],
            type='client',
            allow_unsecure=True
        )

    # TODO : choose a better rappresentation of PlayoffMigration object
    def __str__(self):
        return f'playoff={self._original}' + f'playoff={self._cloned}'

    # ++++++++++++++++++++++++
    # UTILITIES

    def __get_game(self, game: Games):
        """ Return instance of the chosen game """
        if game == Games.original:
            return self._original
        elif game == Games.cloned:
            return self._cloned

    @staticmethod
    def __get_number_pages(number):
        """ Returns the number of pages needed for pagination """
        n_pages = int(number / 100)

        if number % 100 > 0:
            n_pages += 1

        return n_pages

    # ++++++++++++++++++++++++
    # INFORMATION RETRIEVERS

    def get_number_teams(self, game: Games):
        """ Returns the number of teams of the chosen game """
        return self.__get_game(game).get('/admin/teams', {})['total']

    def get_number_players(self, game: Games):
        """ Returns the number of players in the chosen game """
        return self.__get_game(game).get('/admin/players', {})['total']

    def get_number_players_in_team(self, game: Games, team_key):
        """ Returns the number of players in the chosen game """
        return self.__get_game(game).get('/admin/teams/' + team_key + '/members', {})['total']

    def get_game_id(self, game: Games) -> str:
        """ Returns game id of the chosen game """
        return self.__get_game(game).get('/admin')["game"]["id"]

    def get_teams_by_id(self, game: Games):
        """ Returns all the teams ids  """
        teams_id = {}
        count_key = 0
        game_instance = self.__get_game(game)

        for count in range(PlayoffMigration.__get_number_pages(self.get_number_teams(game))):
            teams = game_instance.get('/admin/teams', {"skip": str(count * 100), "limit": "100"})

            for item in teams['data']:
                teams_id.update({count_key: item['id']})
                count_key += 1

        return teams_id

    def get_players_by_id(self, game: Games):
        """ Returns all the ids of the player in the chosen game """
        players_id = {}
        count_key = 0
        game_instance = self.__get_game(game)

        for count in range(PlayoffMigration.__get_number_pages(self.get_number_players(game))):
            players = game_instance.get('/admin/players', {"skip": str(count * 100), "limit": "100"})

            for item in players['data']:
                players_id.update({count_key: item['id']})
                count_key += 1

        return players_id

    def get_players_by_teams(self, game: Games):
        """ Returns all the players grouped by each team of the selected game """
        teams_by_id = self.get_teams_by_id(game)
        players_by_teams = {}

        for key in teams_by_id:
            count_key = 0
            game_instance = self.__get_game(game)

            for count in range(PlayoffMigration.__get_number_pages(self.get_number_players_in_team(game, teams_by_id.get(key)))):
                players_in_team = game_instance.get('/admin/teams/' + teams_by_id.get(key) + '/members',
                                                    {"skip": str(count * 100), "limit": "100"})

                pl_team = {}
                for item in players_in_team['data']:
                    pl_team.update({count_key: item['id']})
                    count_key += 1

                players_by_teams.update({teams_by_id.get(key): pl_team})

        return players_by_teams

    def get_player_feed(self, game: Games, player_id):
        """ Return feed of the chosen player """
        player_feed = self.__get_game(game).get("/admin/players/" + player_id + "/activity", {"start": "0"})
            # list of dict

        if player_feed is None:  # if a player have no feed, GET method return None
            return []

        return player_feed

    def get_teams_design(self, game: Games):
        """ Return teams design of chosen game """
        return self.__get_game(game).get('/design/versions/latest/teams', {})

    def get_single_team_design(self, game: Games, team_id):
        """ Return design of the chosen team in the chosen game """
        return self.__get_game(game).get('/design/versions/latest/teams/' + team_id, {})

    def get_team_instance_info(self, game: Games, team_id):
        """ Return team instance information """
        return self.__get_game(game).get('/admin/teams/' + team_id, {})

    def delete_teams_design(self, game: Games):
        """ Delete team designs in chosen game """
        teams_design = self.get_teams_design(game)

        for team in teams_design:
            self.__get_game(game).delete('/design/versions/latest/teams/' + team['id'], {})

    def delete_teams_instances(self, game: Games):
        """ Delete teams instances in chosen game """
        teams_instance = self.get_teams_by_id(game)

        for team in teams_instance:
            self.__get_game(game).delete('/admin/teams/' + teams_instance.get(team), {})

    # ++++++++++++++++++++++++
    # MIGRATION METHOD

    def migrate_teams_design(self):
        """ Migrate teams design from original game to the cloned one """
        self.delete_teams_design(Games.cloned)  # remove designed team if the exists
        teams_design = self.get_teams_design(Games.original)

        for team in teams_design:
            single_team_design = self.get_single_team_design(Games.original, team['id'])

            # json parameter for post request
            cloned_single_team_design = {
                "name": single_team_design['name'],
                'id': single_team_design['id'],
                'permissions': single_team_design['permissions'],
                'creator_roles': single_team_design['creator_roles'],
                'settings': single_team_design['settings'],
                '_hues': single_team_design['_hues']
            }

            self.__get_game(Games.cloned).post('/design/versions/latest/teams', {}, cloned_single_team_design)

    def migrate_teams_instance(self):
        """ Migrate teams instances from original game to the cloned one """
        self.delete_teams_instances(Games.cloned)
        teams_by_id = self.get_teams_by_id(Games.original)

        for team in teams_by_id:
            team_instance_info = self.get_team_instance_info(Games.original, teams_by_id.get(team))

            cloned_team_instance_info = {
                'id': team_instance_info['id'],
                'name': team_instance_info['name'],
                'access': team_instance_info['access'],
                'definition': team_instance_info['definition']['id']
            }

            self.__get_game(Games.cloned).post('/admin/teams', {}, cloned_team_instance_info)

    def migrate_teams(self):
        self.migrate_teams_design()
        self.migrate_teams_instance()

    # ++++++++++++++++++++++++
    # TEST METHOD


"""
il blocco di codice successivo viene eseguito solo se è il modulo principale
quindi solo se eseguo "python playoff_migration.py"
"""
if __name__ == '__main__':
    p = PlayoffMigration()
    print(p)

    p.migrate_teams_instance()


