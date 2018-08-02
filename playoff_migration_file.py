import os
from json import dump

from refactor_playoff_migration import GetPlayoffDesign, Utility


class ExportDesign(object):

    def __init__(self):
        dir_name = "playoff-data"
        self.dir_path = os.getcwd() + "\\" + dir_name + "\\"

        if not os.path.isdir(self.dir_path):
            os.mkdir(dir_name)

        playoff_client = Utility.get_playoff_client(
            "GAMELABNOTARGETV01_CLIENT_ID",
            "GAMELABNOTARGETV01_CLIENT_SECRET"
        )

        self.design_getter = GetPlayoffDesign(playoff_client)

    def export_teams_design(self):
        """ Create json file containing each team design of the original
        game
        """
        with open(self.dir_path + "teams_design.json", "w+") as file:
            teams_design_clone = {}
            teams_design = self.design_getter.get_teams_design()

            for team in teams_design:
                single_team_design = self.design_getter.get_single_team_design(
                    team['id'])

                team_design_data = {
                    'name': single_team_design['name'],
                    'id': single_team_design['id'],
                    'permissions': single_team_design['permissions'],
                    'creator_roles': single_team_design['creator_roles'],
                    'settings': single_team_design['settings'],
                    '_hues': single_team_design['_hues']
                }

                if 'description' in single_team_design.keys():
                    teams_design_clone.update(
                        {'description': single_team_design['description']})

                teams_design_clone.update({team['id']: team_design_data})

            dump(teams_design_clone, file, sort_keys=True, indent=4)

    def export_metric_design(self):
        """ Create json file containing each metric design of the original
        game
        """
        with open(self.dir_path + "metric_design.json", "w+") as file:
            cloned_metrics = {}
            metrics_design = self.design_getter.get_metrics_design()

            for metric in metrics_design:
                single_metric_design = self.design_getter\
                    .get_single_metric_design(metric['id'])

                metric_design_data = {
                    "id": single_metric_design['id'],
                    "name": single_metric_design['name'],
                    "type": single_metric_design['type'],
                    "constraints": single_metric_design['constraints']
                }

                if "description" in metric_design_data.keys():
                    cloned_metrics.update(
                        {"description": metric_design_data["description"]})

                cloned_metrics.update({metric['id']: metric_design_data})

            dump(cloned_metrics, file, sort_keys=True, indent=4)

    def export_actions_design(self):
        """ Create json file containing each action design of the original
        game
        """
        with open(self.dir_path + "actions_design.json", "w+") as file:
            cloned_actions = {}
            actions_design = self.design_getter.get_actions_design()

            for action in actions_design:
                single_action_design = self.design_getter\
                    .get_single_action_design(action['id'])

                cloned_actions.update({action['id']: single_action_design})

            dump(cloned_actions, file, sort_keys=True, indent=4)

    def export_leaderboards_design(self):
        """ Create json file containing each leaderboard design of the original
        game
        """
        with open(self.dir_path + "leaderboards_design.json", "w+") as file:
            cloned_leaderboards = {}
            leaderboards = self.design_getter.get_leaderboards_design()

            for board in leaderboards:
                single_board = self.design_getter\
                    .get_single_leaderboard_design(board['id'])

                boards_data = {
                    "id": single_board['id'],
                    "name": single_board['name'],
                    "entity_type": single_board['entity_type'],
                    "scope": single_board['scope'],
                    "metric": single_board['metric'],
                    "cycles": single_board['cycles']
                }

                if "description" in single_board.keys():
                    boards_data.update(
                        {"description": single_board["description"]})

                cloned_leaderboards.update({board['id']: boards_data})

            dump(cloned_leaderboards, file, sort_keys=True, indent=4)
