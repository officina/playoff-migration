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
    """ This class implements all the necessary methods and attributes to clone a game and scope its assetts in a
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
        number_teams = self.get_number_teams(game)
        number_pages = PlayoffMigration.__get_number_pages(number_teams)  # pagination management

        for count in range(number_pages):
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
        number_players = self.get_number_players(game)
        number_pages = PlayoffMigration.__get_number_pages(number_players)  # pagination management

        for count in range(number_pages):
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
            number_players_in_team = self.get_number_players_in_team(game, teams_by_id.get(key))
            number_pages = PlayoffMigration.__get_number_pages(number_players_in_team)  # pagination management

            for count in range(number_pages):
                players_in_team = game_instance.get('/admin/teams/' + teams_by_id.get(key) + '/members',
                                                    {"skip": str(count * 100), "limit": "100"})

                pl_team = {}
                for item in players_in_team['data']:
                    pl_team.update({count_key: item['id']})
                    count_key += 1

                players_by_teams.update({teams_by_id.get(key): pl_team})

        return players_by_teams

    def get_player_feed(self, game: Games, player_id):
        """ Return a list containing feed of the chosen player """
        player_feed = self.__get_game(game).get("/admin/players/" + player_id + "/activity", {"start": "0"})

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

    def get_player_profile(self, game: Games, player_id):
        """ Returns the profile data of the selected player """
        return self.__get_game(game).get("/admin/players/" + player_id, {})

    def get_actions_design(self, game: Games):
        """ Returns actions design of the chosen game """
        return self.__get_game(game).get("/design/versions/latest/actions", {})

    def get_single_action_design(self, game: Games, action_id):
        """ Returns a single design of the chosen action in the chosen game """
        return self.__get_game(game).get("/design/versions/latest/actions/" + action_id, {})

    def get_leaderboards_by_id(self, game: Games):
        """ Returns leaderboards by id of the selected game """
        leaderboards_id = []
        leaderboards = self.__get_game(game).get('/design/versions/latest/leaderboards', {})

        for item in leaderboards:
            leaderboards_id.append(item['id'])

        return leaderboards_id

    def get_leaderboard_scope(self, game: Games, leaderboard):
        """ Return scope of chosen leaderboard in the chosen game """
        return self.__get_game(game).get('/design/versions/latest/leaderboards/' + leaderboard, {})['scope']

    # TODO : find a way to not use fixed "player_id"
    def get_leaderboards_players(self, game: Games):
            """ Returns every player and his score, for each leaderboard of the chosen game """
            leaderboards_by_id = self.get_leaderboards_by_id(game)
            leaderboards_content = {}

            for item in leaderboards_by_id:
                leaderboards_scope = self.get_leaderboard_scope(game, item)
                if leaderboards_scope['type'] == 'team_instance':
                    scope_type = leaderboards_scope['id']
                    board_content = self.__get_game(game).get('/runtime/leaderboards/'
                                                              + item, {"cycle": "alltime",
                                                                       "team_instance_id": scope_type,
                                                                       "player_id": "atomasse",
                                                                       "limit": str(10 ** 12)})
                    leaderboards_content.update({item: board_content})

                else:
                    board_content = self.__get_game(game).get('/runtime/leaderboards/'
                                                              + item, {"cycle": "alltime",
                                                                       "player_id": "atomasse",
                                                                       "limit": str(10 ** 12)})
                    leaderboards_content.update({item: board_content})

            return leaderboards_content

    def get_players_with_score_0(self, game: Games):
            """ Return a list containing all the id of the players who have a 0 score in a leaderboard """
            players_zero = []
            leaderboards_players = self.get_leaderboards_players(game)

            for k, v in leaderboards_players.items():
                for player in v['data']:
                    if player['score'] == '0':
                        players_zero.append(player['player']['id'])

            players_zero_def = []
            for item in players_zero:  # removal of the duplicates
                if item not in players_zero_def:
                    players_zero_def.append(item)

            return players_zero_def

    def get_single_leaderboard_design(self, game: Games, leaderboard_id):
        """ Returns a single design of the chosen leaderboard in the chosen game """
        return self.__get_game(game).get("/design/versions/latest/leaderboards/" + leaderboard_id, {})

    def get_metrics_design_id(self, game: Games):
        """ Returns metrics design id """
        return self.__get_game(game).get("/design/versions/latest/metrics", {})

    def get_single_metric_design(self, game: Games, metric_id):
        """ Returns design of the chosen metric """
        return self.__get_game(game).get("/design/versions/latest/metrics/" + metric_id, {})

    # +++++++++++++++++++
    # INFORMATION ERASERS

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

    def delete_player_instances(self, game: Games):
        """ Deletes all the player instances from the selected game"""
        players_instance = self.get_players_by_id(game)
        for player in players_instance:
            self.__get_game(game).delete('/admin/players/' + players_instance.get(player), {})

    def delete_actions_design(self, game: Games):
        """ Delete actions design in chosen game """
        actions_design = self.get_actions_design(game)

        for action in actions_design:
            self.__get_game(game).delete("/design/versions/latest/actions/" + action['id'], {})

    def delete_leaderboards_design(self, game: Games):
        """ Delete leaderboards design in chosen game """
        leaderboards_design = self.get_leaderboards_by_id(game)

        for item in leaderboards_design:
            self.__get_game(game).delete("/design/versions/latest/leaderboards/" + item, {})

    def delete_metrics_design(self, game: Games):
        """ Deletes metrics design in the chosen game"""
        metrics_design_id = self.get_metrics_design_id(game)

        for item in metrics_design_id:
            self.__get_game(game).delete("/design/versions/latest/metrics/" + item['id'], {})

    # ++++++++++++++++++++++++
    # MIGRATION METHODS

    def __migrate_teams_design(self):
        """ Migrate teams design from original game to the cloned one """
        self.delete_teams_design(Games.cloned)  # remove designed team if the exists
        teams_design = self.get_teams_design(Games.original)

        for team in teams_design:
            single_team_design = self.get_single_team_design(Games.original, team['id'])

            # TODO : verifie if is necessary
            # json parameter for post request
            cloned_single_team_design = {
                'name': single_team_design['name'],
                'id': single_team_design['id'],
                'permissions': single_team_design['permissions'],
                'creator_roles': single_team_design['creator_roles'],
                'settings': single_team_design['settings'],
                '_hues': single_team_design['_hues']
            }

            self.__get_game(Games.cloned).post('/design/versions/latest/teams', {}, cloned_single_team_design)

    def __migrate_teams_instances(self):
        """ Migrate teams instances from original game to the cloned one """
        self.delete_teams_instances(Games.cloned)
        teams_by_id = self.get_teams_by_id(Games.original)

        for team in teams_by_id:
            team_instance_info = self.get_team_instance_info(Games.original, teams_by_id.get(team))

            # TODO : check if is necessary
            cloned_team_instance_info = {
                'id': team_instance_info['id'],
                'name': team_instance_info['name'],
                'access': team_instance_info['access'],
                'definition': team_instance_info['definition']['id']
            }

            self.__get_game(Games.cloned).post('/admin/teams', {}, cloned_team_instance_info)

    def __migrate_players(self):
        """ Migrates the player instances from the original game to the cloned one """
        self.delete_player_instances(Games.cloned)
        players_by_id = self.get_players_by_id(Games.original)

        for player in players_by_id:
            player_instance_info = self.get_player_profile(Games.original, players_by_id.get(player))

            cloned_player_instance_info = {
                'id': str(player_instance_info['id']),
                'alias': str(player_instance_info['alias'])}

            self.__get_game(Games.cloned).post('/admin/players', {}, cloned_player_instance_info)

    def __migrate_players_in_team(self):
        """ Migrates players from team in original game to the cloned one """
        players_by_id = self.get_players_by_id(Games.original)

        for key in players_by_id:
            player_id = players_by_id.get(key)
            player_profile = self.get_player_profile(Games.original, player_id)

            for team in player_profile['teams']:
                cloned_team_player = {
                    "requested_roles": {
                        team['roles'][0]: True
                    },
                    "player_id": player_id
                }
                self.__get_game(Games.cloned).post("/admin/teams/" + team['id'] + "/join", {}, cloned_team_player)

    def __migrate_action_design(self):
        self.delete_actions_design(Games.cloned)
        actions_design = self.get_actions_design(Games.original)

        for action in actions_design:
            single_action_design = self.get_single_action_design(Games.original, action['id'])

            single_action_info = {
                "id": single_action_design['id'],
                "name": single_action_design['name'],
                "requires": single_action_design['requires'],
                "rules": single_action_design['rules'],
                "variables": single_action_design['variables']
            }

            self.__get_game(Games.cloned).post("/design/versions/latest/actions", {}, single_action_info)

    def __migrate_players_feed(self):
        """ Migrates players feed from original game to cloned one """
        players_id = self.get_players_by_id(Games.original)

        for key, player_id in players_id.items():
            player_feed = self.get_player_feed(Games.original, player_id)

            for item in player_feed:
                if item['event'] == 'action':
                    action_id = item['action']['id']
                    variables = item['action']['vars']
                    scopes = item['scopes']

                    self.__get_game(Games.cloned).post("/runtime/actions/" + action_id + "/play",
                                                       {"player_id": player_id}, {"variables": variables,
                                                                                  "scopes": scopes})

    def __migrate_leaderboards_design(self):
        self.delete_leaderboards_design(Games.cloned)
        leaderboards_id = p.get_leaderboards_by_id(Games.original)

        for id_lead in leaderboards_id:
            single_design_lead = p.get_single_leaderboard_design(Games.original, id_lead)

            boards_single_design_info = {
                "id": single_design_lead['id'],
                "name": single_design_lead['name'],
                "entity_type": single_design_lead['entity_type'],
                "scope": single_design_lead['scope'],
                "metric": single_design_lead['metric']
            }

            self.__get_game(Games.cloned).post("/design/versions/latest/leaderboards", {}, boards_single_design_info)

    def __migrate_metrics_design(self):
        """ Migrates metrics design from original game to the cloned one """
        self.delete_metrics_design(Games.cloned)
        metrics_design_id = self.get_metrics_design_id(Games.original)

        for item in metrics_design_id:
            single_metric_degign = self.get_single_metric_design(Games.original, item['id'])

            input_metric_design = {
                "id": single_metric_degign['id'],
                "name": single_metric_degign['name'],
                "type": single_metric_degign['type'],
                "constraints": single_metric_degign['constraints']
            }

            self.__get_game(Games.cloned).post("/design/versions/latest/metrics", {}, input_metric_design)

    def migrate(self):
        self.__migrate_teams_design()
        self.__migrate_teams_instances()
        self.__migrate_players()
        self.__migrate_players_in_team()
        self.__migrate_metrics_design()
        self.__migrate_action_design()
        self.__migrate_players_feed()
        self.__migrate_leaderboards_design()

    # +++++++++++++++
    # TEST METHODS

"""
il blocco di codice successivo viene eseguito solo se è il modulo principale
quindi solo se eseguo "python playoff_migration.py"
"""
if __name__ == '__main__':
    p = PlayoffMigration()
    print(p)