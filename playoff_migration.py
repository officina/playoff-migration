from playoff import Playoff, PlayoffException
import os
from dotenv import load_dotenv
from pprint import pprint
from enum import Enum
import sys


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

    def get_game_id(self, game: Games) -> str:
        if game == Games.original:
            return self._original.get('/admin')["game"]["id"]
        elif game == Games.cloned:
            return self._cloned.get('/admin')["game"]["id"]

    # TODO : check if not sorting dict is a problem
    def get_teams(self, game: Games):
        teams = {}
        if game == Games.original:
            teams = self._original.get('/admin/teams', {})
        elif game == Games.cloned:
            teams = self._cloned.get('/admin/teams', {})
        teams_id = {}
        count = 0
        for item in teams['data']:
            teams_id.update({'id' + str(count): item['id']})
            count += 1
        return teams_id

    def get_numbers_players(self, game: Games):
        if game == Games.original:
            return self._original.get('/admin/players', {})['total']
        if game == Games.cloned:
            return self._cloned.get('/admin/players', {})['total']

    # TODO : check if not sorting dict is a problem
    def get_players(self, game: Games):
        number_of_players = str(self.get_numbers_players(game))
        players = {}
        if game == Games.original:
            players = self._original.get('/admin/players', {"limit": "100"})
        elif game == Games.cloned:
            players = self._cloned.get('/admin/players', {"limit": "16"})
        players_id = {}
        count = 0
        for item in players['data']:
            players_id.update({count: item['id']})
            count += 1
        #return players_id
        pprint(players)
        pprint(players_id)

    def check_all_players(self):
        response1 = self._original.get('/admin/players', {})
        response2 = self._cloned.get('/admin/players', {})
        pprint(response1)
        pprint(response2)
        return sorted(response1) == sorted(response2)

    def team_players_match(self):
        teams_game1 = self._original.get('/admin/teams', {})
        teams_game2 = self._cloned.get('/admin/teams', {})
        teams_id_game1 = filter(lambda x: x['id'], teams_game1['data'])

"""
il blocco di codice successivo viene eseguito solo se è il modulo principale
quindi solo se eseguo "python playoff_migration.py"
"""
if __name__ == '__main__':
    p = PlayoffMigration()
    p.get_players(Games.original)
