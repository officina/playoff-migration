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

    def __str__(self):
        return f'playoff={self._original}'

    def get_game_id(self, game: Games) -> str:
        if game == Games.original:
            return self._original.get('/admin')["game"]["id"]
        elif game == Games.cloned:
            return self._cloned.get('/admin')["game"]["id"]

    def check_game(self, game_id: str, client_playoff: Playoff) -> bool:
        # call playoff to check for game with id:
        response = client_playoff.get('/admin')
        pprint(response)
        id = response["game"]["id"]
        print(id)
        return game_id == id

    def check_all_teams(self):
        response1 = self._original.get('/admin/teams', {})
        response2 = self._cloned.get('/admin/teams', {})
        pprint(response1)
        pprint(response2)
        return sorted(response1) == sorted(response2)

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
    print("Eseguito il main di playoff_migration")
    p = PlayoffMigration()
    a = p.check_game('asd', p._original)
    print(a)
