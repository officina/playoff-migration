from playoff import Playoff, PlayoffException
import os
from dotenv import load_dotenv
import json
from pprint import pprint


class PlayoffCreation(object):

    file_path: str

    def __init__(self, file_path):
        self.file_path = file_path
        from pathlib import Path  # python3 only
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)
        self.target = Playoff(
            client_id=os.environ["GAMELAB_GAZZ_STAGING_CLIENT_ID"],
            client_secret=os.environ["GAMELAB_GAZZ_STAGING_CLIENT_SECRET"],
            type='client',
            allow_unsecure=True
        )

    def get_leaderboards_by_id(self):
        """ Returns leaderboards by id of the selected game """
        leaderboards_id = []
        leaderboards = self.target.get('/design/versions/latest/leaderboards', {})

        for item in leaderboards:
            leaderboards_id.append(item['id'])

        return leaderboards_id

    def get_actions_design(self):
        """ Returns actions design of the chosen game """
        return self.target.get("/design/versions/latest/actions", {})

    def get_metrics_design_id(self):
        """ Returns metrics design id """
        return self.target.get("/design/versions/latest/metrics", {})

    def delete_actions_design(self):
        """ Delete actions design in chosen game """
        actions_design = self.get_actions_design(target)

        for action in actions_design:
            self.target.delete("/design/versions/latest/actions/" + action['id'], {})

    def delete_leaderboards_design(self):
        """ Delete leaderboards design in chosen game """
        leaderboards_design = self.get_leaderboards_by_id(target)

        for item in leaderboards_design:
            self.target.delete("/design/versions/latest/leaderboards/" + item, {})

    def delete_metrics_design(self):
        """ Deletes metrics design in the chosen game"""
        metrics_design_id = self.get_metrics_design_id(target)

        for item in metrics_design_id:
            self.target.delete("/design/versions/latest/metrics/" + item['id'], {})

    # OK METHOD

    def import_teams_design(self):
        self.delete_teams_design()

        with open(self.file_path + "teamsDesign.json", "r") as file:
            teams_design = json.load(file)

        for key, value in teams_design.items():
            self.target.post("/design/versions/latest/teams", {}, value)

    def import_teams_instance(self):
        self.delete_teams_instances()

        with open(self.file_path + "teamsInstances.json", "r") as file:
            teams_instance = json.load(file)

        for key, value in teams_instance.items():
            self.target.post("/admin/teams", {}, value)

    def import_players(self):
        self.delete_player_instances()

        with open(self.file_path + "players.json", "r") as file:
            players = json.load(file)

        for key, value in players.items():
            self.target.post('/admin/players', {}, value)

    def delete_teams_design(self):
        """ Delete team designs in chosen game """
        teams_design = self.get_teams_design()

        for team in teams_design:
            self.target.delete('/design/versions/latest/teams/' + team['id'], {})

    def delete_teams_instances(self):
        """ Delete teams instances in chosen game """
        teams_instance = self.get_teams_by_id()

        for team in teams_instance:
            self.target.delete('/admin/teams/' + teams_instance.get(team), {})

    def delete_player_instances(self):
        """ Deletes all the player instances from the selected game"""
        players_instance = self.get_players_by_id()

        for player in players_instance:
            self.target.delete('/admin/players/' + players_instance.get(player), {})

    @staticmethod
    def __get_number_pages(number):
        """ Returns the number of pages needed for pagination """
        n_pages = int(number / 100)

        if number % 100 > 0:
            n_pages += 1

        return n_pages

    def get_number_teams(self):
        """ Returns the number of teams of the chosen game """
        return self.target.get('/admin/teams', {})['total']

    def get_teams_by_id(self):
        """ Returns all the teams ids  """
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

    def get_teams_design(self):
        """ Return teams design of chosen game """
        return self.target.get('/design/versions/latest/teams', {})

    def get_number_players(self):
        return self.target.get('/admin/players', {})['total']

    def get_players_by_id(self):
        """ Returns all the ids of the player in the chosen game """
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

    # def import_player_instances(self):
    #     with open(self.file_path + "teamsInstances.json", "r") as file:
    #         teams_instances = json.load(file)
    #         for key, value in teams_instances.items():




















if __name__ == '__main__':
    pc = PlayoffCreation("C:\\Users\\Loren\\Desktop\\PlayoffData\\")
    # pc.import_teams_design()
    pc.import_teams_design()


