from playoff_migration import PlayoffMigration
from playoff_migration import Games
import json
import os
from dotenv import load_dotenv
import logging
from pprint import pprint


class ExportData(object):
    """ This class purpose is to retrieve data from Playoff game
    (via PlayoffMigration class), processing data to retrieve only useful
    information and store it in json file.
    """

    pm: PlayoffMigration
    __file_path: str

    def __init__(self):
        self._logger = logging.getLogger("export_logger")
        self._logger.setLevel(logging.DEBUG)
        ch = logging.FileHandler(filename="export.log", mode="w")
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - ExportData - %(message)s', '%m/%d/%Y %I:%M:%S %p')
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)
        self._logger.info("running...")

        self.pm = PlayoffMigration()
        from pathlib import Path  # python3 only
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)
        self.__file_path = os.environ["FOLDER_PATH"]

    def __str__(self):
        return self.pm.__str__()

    def export_teams_design(self):
        """ Create json file containing each team design of the original
        game
        """
        self._logger.info(self.export_teams_design.__name__ + " called")

        with open(self.__file_path + "teamsDesign.json", "w+") as file:
            cloned_teams_design = {}
            teams_design = self.pm.get_teams_design(Games.original)

            for team in teams_design:
                single_team_design = self.pm.get_single_team_design(
                    Games.original, team['id'])

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

                cloned_teams_design.update({team['id']:
                                            cloned_single_team_design})

            json.dump(cloned_teams_design, file, sort_keys=True, indent=4)

    def export_metric_design(self):
        """ Create json file containing each metric design of the original game"""
        self._logger.info(self.export_metric_design.__name__ + " called")

        with open(self.__file_path + "metricDesign.json", "w+") as file:
            cloned_metrics_design = {}
            metrics_design_id = self.pm.get_metrics_design_id(Games.original)

            for item in metrics_design_id:
                single_metric_degign = self.pm.get_single_metric_design(Games.original, item['id'])

                input_metric_design = {
                    "id": single_metric_degign['id'],
                    "name": single_metric_degign['name'],
                    "type": single_metric_degign['type'],
                    "constraints": single_metric_degign['constraints']
                }

                cloned_metrics_design.update({item['id']: input_metric_design})

            json.dump(cloned_metrics_design, file, sort_keys=True, indent=4)

    def export_actions_design(self):
        """ Create json file containing each action design of the original game"""
        self._logger.info(self.export_actions_design.__name__ + " called")

        with open(self.__file_path + "actionsDesign.json", "w+") as file:
            cloned_actions_design = {}
            actions_design = self.pm.get_actions_design(Games.original)

            for action in actions_design:
                single_action_design = self.pm.get_single_action_design(Games.original, action['id'])

                cloned_actions_design.update({action['id']: single_action_design})

            json.dump(cloned_actions_design, file, sort_keys=True, indent=4)

    def export_leaderboards_design(self):
        """ Create json file containing each leaderboard design of the original game"""
        self._logger.info(self.export_leaderboards_design.__name__ + " called")

        with open(self.__file_path + "leaderboardsDesign.json", "w+") as file:
            cloned_leaderboards_design = {}
            leaderboards_id = self.pm.get_leaderboards_design_by_id(Games.original)

            for id_lead in leaderboards_id:
                single_design_lead = self.pm.get_single_leaderboard_design(Games.original, id_lead)

                boards_single_design_info = {
                    "id": single_design_lead['id'],
                    "name": single_design_lead['name'],
                    "entity_type": single_design_lead['entity_type'],
                    "scope": single_design_lead['scope'],
                    "metric": single_design_lead['metric']
                }

                cloned_leaderboards_design.update({id_lead: boards_single_design_info})

            json.dump(cloned_leaderboards_design, file, sort_keys=True, indent=4)

    def export_teams_instances(self):
        """ Create json file containing each team instance of the original game"""
        self._logger.info(self.export_teams_instances.__name__ + " called")

        with open(self.__file_path + "teamsInstances.json", "w+") as file:
            cloned_teams_instances = {}
            teams_by_id = self.pm.get_teams_by_id(Games.original)

            for team in teams_by_id:
                team_instance_info = self.pm.get_team_instance_info(Games.original, teams_by_id.get(team))

                cloned_team_instance_info = {
                    'id': team_instance_info['id'],
                    'name': team_instance_info['name'],
                    'access': team_instance_info['access'],
                    'definition': team_instance_info['definition']['id']
                }

                cloned_teams_instances.update({teams_by_id.get(team): cloned_team_instance_info})

            json.dump(cloned_teams_instances, file, sort_keys=True, indent=4)

    def export_players(self):
        """ Create json file containing id and alias of each player of the original game"""
        self._logger.info(self.export_players.__name__ + " called")

        with open(self.__file_path + "players.json", "w+") as file:
            cloned_players = {}
            players_by_id = self.pm.get_players_by_id(Games.original)

            for player in players_by_id:
                player_instance_info = self.pm.get_player_profile(Games.original, players_by_id.get(player))

                cloned_player_instance_info = {
                    'id': str(player_instance_info['id']),
                    'alias': str(player_instance_info['alias'])}

                cloned_players.update({players_by_id.get(player): cloned_player_instance_info})

            json.dump(cloned_players, file, sort_keys=True, indent=4)

    def export_players_in_team(self):
        """ Create json file containing the team of each player of the original game"""
        self._logger.info(self.export_players_in_team.__name__ + " called")

        with open(self.__file_path + "playersInTeam.json", "w+") as file:
            cloned_players_in_team = {}
            players_by_id = self.pm.get_players_by_id(Games.original)

            for key in players_by_id:
                player_id = players_by_id.get(key)
                player_profile = self.pm.get_player_profile(Games.original, player_id)

                for team in player_profile['teams']:

                    cloned_team_player = {
                        "requested_roles": {
                            team['roles'][0]: True
                        },
                        "player_id": player_id
                    }

                    team_id = team['id']

                    if not (team_id in cloned_players_in_team.keys()):
                        cloned_players_in_team.update({team_id: []})
                        cloned_players_in_team[team_id].append(cloned_team_player)
                    else:
                        cloned_players_in_team[team_id].append(cloned_team_player)

            json.dump(cloned_players_in_team, file, sort_keys=True, indent=4)

    def export_players_feed(self):
        """ Create json file containing the activity feed of each player of the original game"""
        self._logger.info(self.export_players_feed.__name__ + " called")

        with open(self.__file_path + "playersFeed.json", "w+") as file:
            cloned_players_feed = {}
            players_id = self.pm.get_players_by_id(Games.original)

            for key, player_id in players_id.items():
                player_feed = self.pm.get_player_feed(Games.original, player_id)

                for item in player_feed:
                    player_single_feed = {}
                    if item['event'] == 'action':
                        player_single_feed.update({"id": item['action']['id']})
                        player_single_feed.update({"variables": item['action']['vars']})
                        player_single_feed.update({"scopes": item['scopes']})

                        if not (player_id in cloned_players_feed.keys()):
                            cloned_players_feed.update({player_id: []})
                            cloned_players_feed[player_id].append(player_single_feed)
                        else:
                            cloned_players_feed[player_id].append(player_single_feed)

            json.dump(cloned_players_feed, file, sort_keys=True, indent=4)

    def export_design(self):
        """Export all design of the original game in a file"""
        self._logger.info("Exporting design...")

        self.export_teams_design()
        self.export_metric_design()
        self.export_actions_design()
        self.export_leaderboards_design()

    def export_istances(self):
        """Export all istances of the original game in a file"""
        self._logger.info("Exporting instances...")

        self.export_teams_instances()
        self.export_players()
        self.export_players_in_team()
        self.export_players_feed()


class ExportRawData(object):
    """ This class purpose is to retrieve data from Playoff game
    (via PlayoffMigration class) and store it in json file.
    """

    pm: PlayoffMigration
    __file_path: str

    def __init__(self):
        self._logger = logging.getLogger("creation_logger")
        self._logger.setLevel(logging.DEBUG)
        ch = logging.FileHandler(filename="export.log", mode="w")
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - ExportRawData - %(message)s',
                                      '%m/%d/%Y %I:%M:%S %p')
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)
        self._logger.info("running...")

        self.pm = PlayoffMigration()

        from pathlib import Path  # python3 only
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)
        self.__file_path = os.environ["FOLDER_PATH"]

    def __str__(self):
        return self.pm.__str__()

    def export_raw_teams_instances(self):
        """Saves raw instances of all teams from the original game in a .json format"""
        self._logger.info(self.export_raw_teams_instances.__name__ + " called")

        with open(self.__file_path + "teams_raw_instances.json", "w+") as file:
            cloned_teams_instances = []
            teams_by_id = self.pm.get_teams_by_id(Games.original)

            for team in teams_by_id:
                team_instance_info = self.pm.get_team_instance_info(Games.original, teams_by_id.get(team))

                cloned_teams_instances.append(team_instance_info)

            for team in cloned_teams_instances:
                json.dump(team, file, sort_keys=True, indent=4)

    def export_raw_players_profile_data(self):
        """Saves raw profile data of all players from the original game in a .json format
        Profile data of a player includes feeds and their teams
        """
        self._logger.info(self.export_raw_players_profile_data.__name__ + " called")

        with open(self.__file_path + "players_raw_profile_data.json", "w+") as file:
            cloned_players = []
            players_by_id = self.pm.get_players_by_id(Games.original)

            for player in players_by_id:
                player_instance_info = self.pm.get_player_profile(Games.original, players_by_id.get(player))

                cloned_players.append(player_instance_info)

            for player in cloned_players:
                json.dump(player, file, sort_keys=True, indent=4)

    def export_raw_teams_design(self):
        """Saves raw teams design data from the original game in a .json file"""
        self._logger.info(self.export_raw_teams_design.__name__ + " called")

        with open(self.__file_path + "teams_raw_design.json", "w+") as file:
            cloned_teams_design = []
            teams_design = self.pm.get_teams_design(Games.original)

            for team in teams_design:
                single_team_design = self.pm.get_single_team_design(Games.original, team['id'])

                cloned_teams_design.append(single_team_design)

            json.dump(cloned_teams_design, file, sort_keys=True, indent=4)

    def export_raw_metrics_design(self):
        """Saves raw metrics design data from the original game in a .json file"""
        self._logger.info(self.export_raw_metrics_design.__name__ + " called")

        with open(self.__file_path + "metrics_raw_design.json", "w+") as file:
            cloned_metrics_design = []
            metrics_design_id = self.pm.get_metrics_design_id(Games.original)

            for item in metrics_design_id:
                single_metric_design = self.pm.get_single_metric_design(Games.original, item['id'])

                cloned_metrics_design.append(single_metric_design)

            json.dump(cloned_metrics_design, file, sort_keys=True, indent=4)

    def export_raw_actions_design(self):
        """Saves raw actions design data from the original game in a .json file"""
        self._logger.info(self.export_raw_actions_design.__name__ + " called")

        with open(self.__file_path + "actions_raw_design.json", "w+") as file:
            cloned_actions_design = []
            actions_design = self.pm.get_actions_design(Games.original)

            for action in actions_design:
                single_action_design = self.pm.get_single_action_design(Games.original, action['id'])

                cloned_actions_design.append(single_action_design)

            json.dump(cloned_actions_design, file, sort_keys=True, indent=4)

    def export_raw_leaderboards_design(self):
        """Saves raw leaderboards design data from the original game in a .json file"""
        self._logger.info(self.export_raw_leaderboards_design.__name__ + " called")

        with open(self.__file_path + "leaderboards_raw_design.json", "w+") as file:
            cloned_leaderboards_design = []
            leaderboards_id = self.pm.get_leaderboards_design_by_id(Games.original)

            for id_lead in leaderboards_id:
                single_design_lead = self.pm.get_single_leaderboard_design(Games.original, id_lead)

                cloned_leaderboards_design.append(single_design_lead)

            json.dump(cloned_leaderboards_design, file, sort_keys=True, indent=4)


if __name__ == '__main__':
    ep = ExportData()
    erp = ExportRawData()
    print(ep)
    print(erp)
