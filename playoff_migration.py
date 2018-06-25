from playoff import Playoff, PlayoffException

class PlayoffMigration(object):

    _playoff:Playoff = None

    def __init__(self, playoff):
        self._playoff = playoff

    def __str__(self):
        return f'playoff={self._playoff}'

    def check_game(self, original_id:str) -> bool:
        # call playoff to check for game with id:
        return false



if __name__ == '__main__':
    pl = Playoff(
        client_id="MjQ5NWMxMTYtMjBjZi00M2IwLTk3NzEtOWM1YWY1ODQ3Mzll",
        client_secret="OTJlZTMzZTAtMzYzOC00ZDNmLTgxZTAtY2QwNjczZGUzODZjNjZhMWY3NjAtMjg5Yy0xMWU4LWE1ZTUtZTlhOTg0MGEwZTFh",
        type='client',
        allow_unsecure = True
    )
    p = PlayoffMigration(pl)
    a = p.clone_game('asd')
    print(a)