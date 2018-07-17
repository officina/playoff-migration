from playoff import Playoff, PlayoffException
import os
from dotenv import load_dotenv
import json
from pprint import pprint


class PlayoffCreation(object):
    """ Purpose of this class is to retrieve information from specific json formatted file e put data in a Playoff game """

    __file_path: str

    def __init__(self):
        from pathlib import Path  # python3 only
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)
        self.target = Playoff(
            client_id=os.environ["GAMELAB_GAZZ_STAGING_CLIENT_ID"],
            client_secret=os.environ["GAMELAB_GAZZ_STAGING_CLIENT_SECRET"],
            type='client',
            allow_unsecure=True
        )
        # TODO: test this statement
        self.__file_path = os.environ["FOLDER_PATH"]

    def __str__(self):
        return f'playoff = {self.target}'

    # +++++++++++++++
    # IMPORT METHODS

    def import_teams_design(self):
        """ Import teams design from file and post them in the game """
        with open(self.__file_path + "teamsDesign.json", "r") as file:
            teams_design = json.load(file)

        for key, value in teams_design.items():
            self.target.post("/design/versions/latest/teams", {}, value)

    def import_teams_instance(self):
        """ Import teams instances from file and post them in the game """
        with open(self.__file_path + "teamsInstances.json", "r") as file:
            teams_instance = json.load(file)

        for key, value in teams_instance.items():
            self.target.post("/admin/teams", {}, value)

    def import_players(self):
        """ Import players from file and post them in the game """
        with open(self.__file_path + "players.json", "r") as file:
            players = json.load(file)

        for key, value in players.items():
            self.target.post('/admin/players', {}, value)

    def import_players_in_team(self):
        """ Import players in teams from file and post them in the game """
        with open(self.__file_path + "playersInTeam.json", "r") as file:
            players_team = json.load(file)

        for key, value in players_team.items():
            self.target.post("/admin/teams/" + key + "/join", {}, value)

    def import_metric_design(self):
        """ Import metrics design from file and post them in the game """
        with open(self.__file_path + "metricDesign.json", "r") as file:
            metrics_design = json.load(file)

        for key, value in metrics_design.items():
            self.target.post("/design/versions/latest/metrics", {}, value)

    def import_action_design(self):
        """ Import actions design from file and post them in the game """
        with open(self.__file_path + "actionsDesign.json", "r") as file:
            actions_design = json.load(file)

        for key, value in actions_design.items():
            self.target.post("/design/versions/latest/actions", {}, value)

    def import_players_feed(self):
        """ Import players feed from file and post them in the game """
        with open(self.__file_path + "playersFeed.json", "r") as file:
            players_feed = json.load(file)

        for player_id, value in players_feed.items():
            self.target.post("/runtime/actions/" + value['id'] + "/play",
                             {"player_id": player_id}, {"variables": value['variables'], "scopes": value['scopes']})

    def import_leaderboard_design(self):
        """ Import leaderboard design from file and post them in the game """
        with open(self.__file_path + "leaderboardsDesign.json", "r") as file:
            leaderboards_design = json.load(file)

        for key, value in leaderboards_design.items():
            self.target.post("/design/versions/latest/leaderboards", {}, value)

    def import_all_design(self):
        self.import_teams_design()
        self.import_metric_design()
        self.import_action_design()
        self.import_leaderboard_design()

    def import_all_istances(self):
        """ Import all data in the game """
        self.import_teams_instance()
        self.import_players()
        self.import_players_feed()

    # +++++++++++++++++++
    # INFORMATION ERASERS

    def delete_leaderboards_design(self):
        """ Delete leaderboards design in the game """
        leaderboards_design = self.get_leaderboards_by_id()

        for item in leaderboards_design:
            self.target.delete("/design/versions/latest/leaderboards/" + item, {})

    def delete_actions_design(self):
        """ Delete actions design in the game """
        actions_design = self.get_actions_design()

        for action in actions_design:
            self.target.delete("/design/versions/latest/actions/" + action['id'], {})

    def delete_metrics_design(self):
        """ Deletes metrics design in the game"""
        metrics_design_id = self.get_metrics_design_id()

        for item in metrics_design_id:
            self.target.delete("/design/versions/latest/metrics/" + item['id'], {})

    def delete_player_instances(self):
        """ Deletes all players in the game"""
        players_instance = self.get_players_by_id()

        for player in players_instance:
            self.target.delete('/admin/players/' + players_instance.get(player), {})

    def delete_teams_instances(self):
        """ Delete teams instances in the game """
        teams_instance = self.get_teams_by_id()

        for team in teams_instance:
            self.target.delete('/admin/teams/' + teams_instance.get(team), {})

    def delete_teams_design(self):
        """ Delete teams design in the game """
        teams_design = self.get_teams_design()

        for team in teams_design:
            self.target.delete('/design/versions/latest/teams/' + team['id'], {})

    def delete_all_design(self):
        self.delete_leaderboards_design()
        self.delete_actions_design()
        self.delete_metrics_design()
        self.delete_teams_design()

    def delete_all_istances(self):
        """ Delete all info in the game """
        self.delete_player_instances()
        self.delete_teams_instances()


    # +++++++++++++++++++++
    # INFORMATION RETRIEVER

    @staticmethod
    def __get_number_pages(number):
        """ Returns the number of pages needed for pagination """
        n_pages = int(number / 100)

        if number % 100 > 0:
            n_pages += 1

        return n_pages

    def get_number_teams(self):
        """ Returns number of teams in the game """
        return self.target.get('/admin/teams', {})['total']

    def get_number_players(self):
        """ Returns number of players in the game """
        return self.target.get('/admin/players', {})['total']

    def get_teams_design(self):
        """ Return teams design of the game """
        return self.target.get('/design/versions/latest/teams', {})

    def get_teams_by_id(self):
        """ Returns all teams id in the game """
        teams_id = {}
        count_key = 0
        number_teams = self.get_number_teams()
        number_pages = self.__get_number_pages(number_teams)  # pagination management

        for count in range(number_pages):
            teams = self.target.get('/admin/teams', {"skip": str(count * 100), "limit": "100"})

            for item in teams['data']:
                teams_id.update({count_key: item['id']})
                count_key += 1

        return teams_id

    def get_players_by_id(self):
        """ Returns all players id in the game """
        players_id = {}
        count_key = 0
        number_players = self.get_number_players()
        number_pages = self.__get_number_pages(number_players)  # pagination management

        for count in range(number_pages):
            players = self.target.get('/admin/players', {"skip": str(count * 100), "limit": "100"})

            for item in players['data']:
                players_id.update({count_key: item['id']})
                count_key += 1

        return players_id

    def get_metrics_design_id(self):
        """ Returns metrics design id in the game """
        return self.target.get("/design/versions/latest/metrics", {})

    def get_actions_design(self):
        """ Returns actions design of the the game """
        return self.target.get("/design/versions/latest/actions", {})

    def get_leaderboards_by_id(self):
        """ Returns leaderboards id in the game """
        leaderboards_id = []
        leaderboards = self.target.get('/design/versions/latest/leaderboards', {})

        for item in leaderboards:
            leaderboards_id.append(item['id'])

        return leaderboards_id


if __name__ == '__main__':
    pc = PlayoffCreation()
    pprint(pc)
