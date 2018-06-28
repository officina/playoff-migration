from playoff import Playoff, PlayoffException
import os
from dotenv import load_dotenv
from pprint import pprint
from enum import Enum



class Games(Enum):
    original = "original"
    cloned = "cloned"


class PlayoffMigration(object):

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

    # TODO : is there a way to make this private?
    def pagination_iterations(self, number):
        number_of_iteration = int(number / 100)

        if number % 100 > 0:
            number_of_iteration += 1

        return number_of_iteration

    def get_game_id(self, game: Games) -> str:
        if game == Games.original:
            return self._original.get('/admin')["game"]["id"]
        elif game == Games.cloned:
            return self._cloned.get('/admin')["game"]["id"]

    def get_number_teams(self, game: Games):
        if game == Games.original:
            return self._original.get('/admin/teams', {})['total']
        elif game == Games.cloned:
            return self._cloned.get('/admin/teams', {})['total']

    # TODO : check if not sorting dict is a problem
    def get_teams_by_id(self, game: Games):
        teams = {}
        teams_id = {}
        count_key = 0

        for count in range(self.pagination_iterations(self.get_number_teams(game))):
            if game == Games.original:
                teams = self._original.get('/admin/teams', {"skip": str(count * 100), "limit": "100"})
            elif game == Games.cloned:
                teams = self._cloned.get('/admin/teams', {"skip": str(count * 100), "limit": "100"})

            for item in teams['data']:
                teams_id.update({count_key: item['id']})
                count_key += 1

        return teams_id

    def get_number_players(self, game: Games):
        if game == Games.original:
            return self._original.get('/admin/players', {})['total']
        elif game == Games.cloned:
            return self._cloned.get('/admin/players', {})['total']

    # TODO : check if not sorting dict is a problem
    def get_players_by_id(self, game: Games):
        players_id = {}
        count_key = 0
        players = {}

        for count in range(self.pagination_iterations(self.get_number_players(game))):
            if game == Games.original:
                players = self._original.get('/admin/players', {"skip": str(count * 100), "limit": "100"})
            elif game == Games.cloned:
                players = self._cloned.get('/admin/players', {"skip": str(count * 100), "limit": "100"})

            for item in players['data']:
                players_id.update({count_key: item['id']})
                count_key += 1

        return players_id

    def get_number_players_in_team(self, game: Games, team_key):
        if game == Games.original:
            return self._original.get('/admin/teams/' + team_key + '/members', {})['total']
        elif game == Games.cloned:
            return self._cloned.get('/admin/teams/' + team_key + '/members', {})['total']

    def get_players_by_teams(self, game: Games):
        teams_by_id = self.get_teams_by_id(game)
        players_by_teams = {}

        for key in teams_by_id:
            players_in_team = {}
            count_key = 0

            for count in range(self.pagination_iterations(self.get_number_players_in_team(game, teams_by_id.get(key)))):
                if game == Games.original:
                    players_in_team = self._original.get('/admin/teams/' + teams_by_id.get(key) + '/members',
                                                         {"skip": str(count * 100), "limit": "100"})
                elif game == Games.cloned:
                    players_in_team = self._cloned.get('/admin/teams/' + teams_by_id.get(key) + '/members',
                                                       {"skip": str(count * 100), "limit": "100"})

                pl_team = {}
                for item in players_in_team['data']:
                    pl_team.update({count_key: item['id']})
                    count_key += 1

                players_by_teams.update({teams_by_id.get(key): pl_team})

        return players_by_teams



"""
il blocco di codice successivo viene eseguito solo se è il modulo principale
quindi solo se eseguo "python playoff_migration.py"
"""
if __name__ == '__main__':
    p = PlayoffMigration()
    pprint(p.get_players_by_teams(Games.original))

