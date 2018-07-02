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

    def get_players_feed(self, game: Games, player_id):  # manca un parametro? (i giocatori?)
        pass

    def get_game_leaderboards_list(self, game:Games):
        """Returns the leaderboards of the selected game"""
        leaderboards_name = []
        leaderboards = self.__get_game(game).get('/design/versions/latest/leaderboards',{})
        for item in leaderboards:
            leaderboards_name.append(item['id'])
        return leaderboards_name

    def get_leaderboard_scope(self, game: Games, leaderboard):
        return self.__get_game(game).get('/design/versions/latest/leaderboards/'+ leaderboard, { "player_id" : "atomasse"})['scope']

    def get_leaderboards_players(self, game:Games):
        """ Returns a dict containing every player for each team of the selected game """
        boards = self.get_game_leaderboards_list(game)
        leaderboards_content = {}

        for item in boards:
            if self.get_leaderboard_scope(game, item)['type'] == 'team_instance':
                scope_type = self.get_leaderboard_scope(game, item)['id']
                board_content = self.__get_game(game).get('/runtime/leaderboards/' + str(item),{"cycle" : "alltime", "team_instance_id"
                                                                              : scope_type ,  "player_id" : "atomasse", "limit" : str(10**12)})

                leaderboards_content.update({item : board_content})

            else:
                leaderboards_content.update({item: self.__get_game(game).get('/runtime/leaderboards/' + str(item),
                                                                             {"cycle": "alltime", "player_id": "atomasse",
                                                                              "limit": str(10**12)})})
        return leaderboards_content

    def get_players_with_score_0(self, game:Games):
        """ returns a list containing all the id of the players who have a 0 score in a leaderboard """
        players_zero = []
        leaderboards_players = self.get_leaderboards_players(game)

        for k, v in leaderboards_players.items():
            for player in v['data']:
                if player['score'] == '0':
                    players_zero.append(player['player']['id'])

        players_zero_def = []
        for item in players_zero: #removal of the duplicates
            if item not in players_zero_def:
                players_zero_def.append(item)

        return(players_zero_def)

"""
il blocco di codice successivo viene eseguito solo se è il modulo principale
quindi solo se eseguo "python playoff_migration.py"
"""
if __name__ == '__main__':
    p = PlayoffMigration()
    # pprint(p.get_game_id(Games.original))
    # pprint(p.get_game_id(Games.cloned))
    pprint(p.get_players_with_score_0(Games.original))
