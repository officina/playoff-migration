import os
from enum import Enum
from pprint import pprint
import logging

from playoff import Playoff, PlayoffException
from dotenv import load_dotenv


class Games(Enum):
    """ Enumeration type that identifies each different game """
    original = "original"
    cloned = "cloned"
    scoped = "scoped"


class PlayoffMigration(object):
    """ This class implements all the necessary methods and attributes to clone a game and scope its assetts in a
    second one """
    ACTION_LEADERBOARD_PARSER = {
        "sfida_circle_the_dot": "globale_punti_circle_the_dot_scoped",
        "sfida_circle_the_dot_reset": "globale_punti_circle_the_dot_scoped",
        "sfida_circledot": "globale_punti_circle_dot_scoped",
        "sfida_circledot_reset": "globale_punti_circle_dot_scoped",
        "sfida_color_flow": "globale_punti_color_flow_scoped",
        "sfida_color_flow_reset": "globale_punti_color_flow_scoped",
        "sfida_draw_line": "globale_punti_draw_line_scoped",
        "sfida_draw_line_reset": "globale_punti_draw_line_scoped",
        "sfida_electrio": "globale_punti_electrio",
        "sfida_electrio_reset": "globale_punti_electrio",
        "sfida_engineerio": "globale_punti_engineerio",
        "sfida_engineerio_reset": "globale_punti_engineerio",
        "sfida_focus": "globale_punti_focus",
        "sfida_focus_reset": "globale_punti_focus",
        "sfida_gummy_block": "globale_punti_gummy_block",
        "sfida_gummy_block_reset": "globale_punti_gummy_block",
        "sfida_light_color": "globale_punti_light_color",
        "sfida_light_color_reset": "globale_punti_light_color",
        "sfida_lights": "globale_punti_lights",
        "sfida_lights_reset": "globale_punti_lights",
        "sfida_line_follower": "globale_punti_line_follower",
        "sfida_line_follower_reset": "globale_punti_line_follower",
        "sfida_make7": "globale_punti_make7",
        "sfida_make7_reset": "globale_punti_make7",
        "sfida_parity_with_number": "globale_punti_parity_with_number",
        "sfida_parity_with_number_reset": "globale_punti_parity_with_number",
        "sfida_swappy_balls": "globale_punti_swappy_balls",
        "sfida_swappy_balls_reset": "globale_punti_swappy_balls",
        "sfida_thief_challenge": "globale_punti_thief_challenge",
        "sfida_thief_challenge_reset": "globale_punti_thief_challenge",
    }

    _original: Playoff
    _cloned: Playoff
    _scoped: Playoff

    def __init__(self):
        self._logger = logging.getLogger("migration_logger")
        self._logger.setLevel(logging.DEBUG)
        ch = logging.FileHandler(filename="migration.log", mode="w")
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%m/%d/%Y %I:%M:%S %p')
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)
        self._logger.info("PlayoffMigration logger is running...")

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
            client_id=os.environ["GAMELABCLONSCOPED2_CLIENT_ID"],
            client_secret=os.environ["GAMELABCLONSCOPED2_CLIENT_SECRET"],
            type='client',
            allow_unsecure=True
        )
        self._scoped = Playoff(
            client_id=os.environ["GAMELABCLONSCOPED3_CLIENT_ID"],
            client_secret=os.environ["GAMELABCLONSCOPED3_CLIENT_SECRET"],
            type='client',
            allow_unsecure=True
        )

    def __str__(self):
        return f'playoff={self._original}' + f'playoff={self._cloned}' + f'playoff={self._scoped}'

    # ++++++++++++++++++++++++
    # UTILITIES

    def __get_game(self, game: Games):
        """ Return instance of the chosen game """
        if game == Games.original:
            return self._original
        elif game == Games.cloned:
            return self._cloned
        elif game == Games.scoped:
            return self._scoped

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
        self._logger.info(self.get_teams_by_id.__name__ + " called")

        teams_id = []
        game_instance = self.__get_game(game)
        number_teams = self.get_number_teams(game)
        number_pages = PlayoffMigration.__get_number_pages(number_teams)

        for count in range(number_pages):

            teams = game_instance.get('/admin/teams', {"skip": str(count * 100), "limit": "100"})

            for item in teams['data']:
                teams_id.append(item['id'])

        return teams_id

    def get_players_by_id(self, game: Games):
        """ Returns all the ids of the player in the chosen game """
        self._logger.info(self.get_players_by_id.__name__ + " called")

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
        self._logger.info(self.get_players_by_teams.__name__ + " called")

        teams_by_id = self.get_teams_by_id(game)
        players_by_teams = {}

        for team in teams_by_id:
            count_key = 0
            game_instance = self.__get_game(game)
            number_players_in_team = self.get_number_players_in_team(game, team)
            number_pages = PlayoffMigration.__get_number_pages(number_players_in_team)  # pagination management

            for count in range(number_pages):
                players_in_team = game_instance.get('/admin/teams/' + team + '/members',
                                                    {"skip": str(count * 100), "limit": "100"})

                pl_team = {}
                for item in players_in_team['data']:
                    pl_team.update({count_key: item['id']})
                    count_key += 1

                players_by_teams.update({team: pl_team})

        return players_by_teams

    def get_player_feed(self, game: Games, player_id):
        """ Return a list containing feed of the chosen player """
        self._logger.info(self.get_player_feed.__name__ + " called")

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
            self._logger.info(self.get_leaderboards_players.__name__ + " called")

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
            self._logger.info(self.get_players_with_score_0.__name__ + " called")

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
        self._logger.info(self.delete_teams_design.__name__ + " called")

        teams_design = self.get_teams_design(game)

        for team in teams_design:
            self.__get_game(game).delete('/design/versions/latest/teams/' + team['id'], {})

    def delete_teams_instances(self, game: Games):
        """ Delete teams instances in chosen game """
        self._logger.info(self.delete_teams_instances.__name__ + " called")

        teams_instance = self.get_teams_by_id(game)

        for team in teams_instance:
            self.__get_game(game).delete('/admin/teams/' + team, {})

    def delete_player_instances(self, game: Games):
        """ Deletes all the player instances from the selected game"""
        self._logger.info(self.delete_player_instances.__name__ + " called")

        players_instance = self.get_players_by_id(game)
        for player in players_instance:
            self.__get_game(game).delete('/admin/players/' + players_instance.get(player), {})

    def delete_actions_design(self, game: Games):
        """ Delete actions design in chosen game """
        self._logger.info(self.delete_actions_design.__name__ + " called")

        actions_design = self.get_actions_design(game)

        for action in actions_design:
            self.__get_game(game).delete("/design/versions/latest/actions/" + action['id'], {})

    def delete_leaderboards_design(self, game: Games):
        """ Delete leaderboards design in chosen game """
        self._logger.info(self.delete_leaderboards_design.__name__ + " called")

        leaderboards_design = self.get_leaderboards_by_id(game)

        for item in leaderboards_design:
            self.__get_game(game).delete("/design/versions/latest/leaderboards/" + item, {})

    def delete_metrics_design(self, game: Games):
        """ Deletes metrics design in the chosen game"""
        self._logger.info(self.delete_metrics_design.__name__ + " called")

        metrics_design_id = self.get_metrics_design_id(game)

        for item in metrics_design_id:
            self.__get_game(game).delete("/design/versions/latest/metrics/" + item['id'], {})

    def delete_all_design(self, game: Games):
        """Deletes every design from the chosen game"""
        self._logger.info("Deleting design...")

        self.delete_leaderboards_design(game)
        self.delete_actions_design(game)
        self.delete_metrics_design(game)
        self.delete_teams_design(game)

        self._logger.info("Deleted design")

    def delete_all_istances(self, game: Games):
        """Deletes every istances from the chosen game"""
        self._logger.info("Deleting instances...")

        self.delete_player_instances(game)
        self.delete_teams_instances(game)

        self._logger.info("Deleted instances")

    # ++++++++++++++++++++++++
    # MIGRATION METHODS

    def migrate_teams_design(self, game: Games):
        """ Migrate teams design from original game to the cloned one """
        self._logger.info(self.migrate_teams_design.__name__ + " called")

        teams_design = self.get_teams_design(Games.original)

        for team in teams_design:
            single_team_design = self.get_single_team_design(Games.original, team['id'])

            # TODO : check if it's necessary
            # json parameter for post request
            cloned_single_team_design = {
                'name': single_team_design['name'],
                'id': single_team_design['id'],
                'permissions': single_team_design['permissions'],
                'creator_roles': single_team_design['creator_roles'],
                'settings': single_team_design['settings'],
                '_hues': single_team_design['_hues']
            }

            self.__get_game(game).post('/design/versions/latest/teams', {}, cloned_single_team_design)

    def migrate_teams_instances(self, game: Games):
        """ Migrate teams instances from original game to the cloned one """
        self._logger.info(self.migrate_teams_instances.__name__ + " called")

        teams_by_id = self.get_teams_by_id(Games.original)

        for team in teams_by_id:
            team_instance_info = self.get_team_instance_info(Games.original, team)

            # TODO : check if it's necessary
            cloned_team_instance_info = {
                'id': team_instance_info['id'],
                'name': team_instance_info['name'],
                'access': team_instance_info['access'],
                'definition': team_instance_info['definition']['id']
            }

            self.__get_game(game).post('/admin/teams', {}, cloned_team_instance_info)

    def migrate_players(self, game: Games):
        """ Migrates the player instances from the original game to the cloned one """
        self._logger.info(self.migrate_players.__name__ + " called")

        players_by_id = self.get_players_by_id(Games.original)

        for player in players_by_id:
            player_instance_info = self.get_player_profile(Games.original, players_by_id.get(player))

            cloned_player_instance_info = {
                'id': str(player_instance_info['id']),
                'alias': str(player_instance_info['alias'])}

            self.__get_game(game).post('/admin/players', {}, cloned_player_instance_info)

    def migrate_players_in_team(self, game: Games):
        """ Migrates players from team in original game to the cloned one """
        self._logger.info(self.migrate_players_in_team.__name__ + " called")

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
                self.__get_game(game).post("/admin/teams/" + team['id'] + "/join", {}, cloned_team_player)

    def migrate_metrics_design(self, game: Games):
        """ Migrates metrics design from original game to the cloned one """
        self._logger.info(self.migrate_metrics_design.__name__ + " called")

        metrics_design_id = self.get_metrics_design_id(Games.original)

        for item in metrics_design_id:
            single_metric_design = self.get_single_metric_design(Games.original, item['id'])

            input_metric_design = {
                "id": single_metric_design['id'],
                "name": single_metric_design['name'],
                "type": single_metric_design['type'],
                "constraints": single_metric_design['constraints']
            }

            self.__get_game(game).post("/design/versions/latest/metrics", {}, input_metric_design)

    def migrate_action_design(self, game: Games):
        """ Migrates actions design from original game to the cloned one """
        self._logger.info(self.migrate_action_design.__name__ + " called")

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

            self.__get_game(game).post("/design/versions/latest/actions", {}, single_action_info)

    def migrate_players_feed(self, game: Games):
        """Migrates players feed from original game to cloned one"""
        self._logger.info(self.migrate_players_feed.__name__ + " called")

        players_id = self.get_players_by_id(Games.original)

        for key, player_id in players_id.items():
            player_feed = self.get_player_feed(Games.original, player_id)

            for item in player_feed:
                if item['event'] == 'action':
                    action_id = item['action']['id']
                    variables = item['action']['vars']
                    scopes = item['scopes']

                    self.__get_game(game).post("/runtime/actions/" + action_id + "/play",
                                                       {"player_id": player_id}, {"variables": variables,
                                                                                  "scopes": scopes})

    def migrate_leaderboards_design(self, game: Games):
        """Migrates leaderboards design from original game to cloned one"""
        self._logger.info(self.migrate_leaderboards_design.__name__ + " called")

        leaderboards_id = self.get_leaderboards_by_id(Games.original)

        for id_lead in leaderboards_id:
            single_design_lead = self.get_single_leaderboard_design(Games.original, id_lead)

            boards_single_design_info = {
                "id": single_design_lead['id'],
                "name": single_design_lead['name'],
                "entity_type": single_design_lead['entity_type'],
                "scope": single_design_lead['scope'],
                "metric": single_design_lead['metric']
            }

            self.__get_game(game).post("/design/versions/latest/leaderboards", {}, boards_single_design_info)

    def migrate_all_design(self, game: Games):
        """Migrates all design from original game to the cloned ones"""
        self._logger.info("Migrating design...")

        self.migrate_teams_design(game)
        self.migrate_metrics_design(game)
        self.migrate_action_design(game)
        self.migrate_leaderboards_design(game)

        self._logger.info("Migrating design finished")

    def migrate_all_istances(self, game: Games):
        """Migrates all istances from original game to the cloned ones"""
        self._logger.info("Migrating instances...")

        self.migrate_teams_instances(game)
        self.migrate_players(game)
        self.migrate_players_in_team(game)
        self.migrate_players_feed(game)

        self._logger.info("Migrating instances finished")

    # ++++++++++++++++++++++++
    # SCOPED METHODS

    def migrate_scoped_leaderboards_design(self, game: Games):
        """Migrates scoped leaderboards design from original game to cloned one"""
        self._logger.info(self.migrate_scoped_leaderboards_design.__name__ + " called")

        leaderboards_id = self.get_leaderboards_by_id(Games.original)

        for id_lead in leaderboards_id:
            single_design_lead = self.get_single_leaderboard_design(Games.original, id_lead)

            boards_single_design_info = {
                "id": single_design_lead['id'],
                "name": single_design_lead['name'],
                "entity_type": single_design_lead['entity_type'],
                "scope": {"type": "custom"},
                "metric": single_design_lead['metric']
            }

            self.__get_game(game).post("/design/versions/latest/leaderboards", {}, boards_single_design_info)

    def migrate_scoped_players_feed(self, game: Games):
        """Migrates scoped players feed from original game to cloned one"""
        self._logger.info(self.migrate_scoped_players_feed.__name__ + " called")

        players_id = self.get_players_by_id(Games.original)

        for key, player_id in players_id.items():
            player_feed = self.get_player_feed(Games.original, player_id)
            player_profile = self.get_player_profile(Games.original, player_id)
            players_teams = player_profile["teams"]

            for item in player_feed:
                if item['event'] == 'action':
                    action_id = item['action']['id']
                    variables = item['action']['vars']
                    scopes = {}

                    for team in players_teams:
                        if team["id"] == "globale":
                            scopes = self.get_globale_scopes(player_id, action_id)
                            break
                        elif team["id"] == "laboratorio_somma":
                            scopes = self.get_lab_somma_scopes(player_id)
                            break

                    if scopes == {}:
                        scopes = item['scopes']

                    self.__get_game(game).post("/runtime/actions/" + action_id + "/play",
                                               {"player_id": player_id}, {"variables": variables, "scopes": scopes})

    def migrate_all_design_scoped(self, game: Games):
        """Migrates all design from original game to the cloned ones"""
        self._logger.info("Migrating design...")

        self.migrate_teams_design(game)
        self.migrate_metrics_design(game)
        self.migrate_action_design(game)
        self.migrate_scoped_leaderboards_design(game)

        self._logger.info("Migrating design finished")

    def migrate_all_istances_scoped(self, game: Games):
        """Migrates all istances from original game to the cloned ones"""
        self._logger.info("Migrating instances...")

        self.migrate_teams_instances(game)
        self.migrate_players(game)
        self.migrate_players_in_team(game)
        self.migrate_scoped_players_feed(game)

        self._logger.info("Migrating instances finished")

    def get_globale_scopes(self, player_id, action_id):
        return [{
                    "id": "globale_creativita",
                    "entity_id": player_id
                },
                {
                    "id": "globale_problem_solving",
                    "entity_id": player_id
                },
                {
                    "id": "globale_logica",
                    "entity_id": player_id
                },
                {
                    "id": "globale_punti",
                    "entity_id": player_id
                },
                {
                    "id": self.ACTION_LEADERBOARD_PARSER[action_id],
                    "entity_id": player_id
                }]

    def get_lab_somma_scopes(self, player_id):
        return [{
                    "id": "tra_team_creativita",
                    "entity_id": player_id
                },
                {
                    "id": "tra_team_logica",
                    "entity_id": player_id
                },
                {
                    "id": "tra_team_problem_solving",
                    "entity_id": player_id
                },
                {
                    "id": "tra_team_punti",
                    "entity_id": player_id
                }]

    def get_scoped_leaderboard(self, game: Games, leaderboard_id):
        game_instance = self.__get_game(game)

        data = {
            "player_id": "atomasse",
            "cycle": "alltime",
            "limit": 10 ** 10,
            "scope_id": leaderboard_id
        }

        return game_instance.get("/runtime/leaderboards/" + leaderboard_id, data)

    def get_leaderboard(self, game: Games, leaderboard_id):
        game_instance = self.__get_game(game)

        data = {
            "player_id": "atomasse",
            "cycle": "alltime",
            "limit": 10 ** 10,
        }

        return game_instance.get("/runtime/leaderboards/" + leaderboard_id, data)


if __name__ == '__main__':
    p = PlayoffMigration()
    print(p)
