from playoff import Playoff, PlayoffException
import os
from dotenv import load_dotenv

class PlayoffMigration(object):

    _pl:Playoff = None

    def __init__(self):
        from pathlib import Path  # python3 only
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)
        self._pl = Playoff(
        client_id=os.environ["PLAYOFF_CLIENT_ID"],
        client_secret=os.environ["PLAYOFF_CLIENT_SECRET"],
        type='client',
        allow_unsecure=True
        )

    def __str__(self):
        return f'playoff={self._pl}'


    def check_game(self, game_id:str) -> bool:
        # call playoff to check for game with id:
        response = self._pl.get('/admin')
        print(response)
        id = response["game"]["id"]
        print(id)
        return game_id == id




if __name__ == '__main__':

    p = PlayoffMigration()
    a = p.check_game('asd')
    print(a)