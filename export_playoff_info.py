from playoff_migration import PlayoffMigration
from playoff_migration import Games
import json
import os
from dotenv import load_dotenv


class ExportPlayoff(object):
    """ This class purpose is to retrieve data from Playoff game (via PlayoffMigration class) and store it in json
    file
    """

    pm: PlayoffMigration()
    __file_path: str

    def __init__(self):
        self.pm = PlayoffMigration()
        from pathlib import Path  # python3 only
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)
        # TODO: test this statement
        self.__file_path = os.environ["FOLDER_PATH"]

    def __str__(self):
        return self.pm.__str__()

    def export_teams_design(self):
        """ Create json file containing each team design of the original game"""
        with open(self.__file_path + "teamsDesign.json", "w+") as file:
            cloned_teams_design = {}
            teams_design = self.pm.get_teams_design(Games.original)

            for team in teams_design:
                single_team_design = self.pm.get_single_team_design(Games.original, team['id'])

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

                cloned_teams_design.update({team['id']: cloned_single_team_design})

            json.dump(cloned_teams_design, file, sort_keys=True, indent=4)

    def export_teams_instances(self):
        """ Create json file containing each team instance of the original game"""
        with open(self.__file_path + "teamsInstances.json", "w+") as file:
            cloned_teams_instances = {}
            teams_by_id = self.pm.get_teams_by_id(Games.original)

            for team in teams_by_id:
                team_instance_info = self.pm.get_team_instance_info(Games.original, teams_by_id.get(team))

                # TODO : check if is necessary
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

                    cloned_players_in_team.update({team['id']: cloned_team_player})

            json.dump(cloned_players_in_team, file, sort_keys=True, indent=4)

    def export_metric_design(self):
        """ Create json file containing each metric design of the original game"""
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
        with open(self.__file_path + "actionsDesign.json", "w+") as file:
            cloned_actions_design = {}
            actions_design = self.pm.get_actions_design(Games.original)

            for action in actions_design:
                single_action_design = self.pm.get_single_action_design(Games.original, action['id'])

                single_action_info = {
                    "id": single_action_design['id'],
                    "name": single_action_design['name'],
                    "requires": single_action_design['requires'],
                    "rules": single_action_design['rules'],
                    "variables": single_action_design['variables']
                }

                cloned_actions_design.update({action['id']: single_action_design})

            json.dump(cloned_actions_design, file, sort_keys=True, indent=4)

    def export_players_feed(self):
        """ Create json file containing the activity feed of each player of the original game"""
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

                        cloned_players_feed.update({player_id: player_single_feed})

            json.dump(cloned_players_feed, file, sort_keys=True, indent=4)

    def export_leaderboards_design(self):
        """ Create json file containing each leaderboard design of the original game"""
        with open(self.__file_path + "leaderboardsDesign.json", "w+") as file:
            cloned_leaderboards_design = {}
            leaderboards_id = self.pm.get_leaderboards_by_id(Games.original)

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

    def export_design(self):
        self.export_teams_design()
        self.export_metric_design()
        self.export_actions_design()
        self.export_leaderboards_design()

    def export_istances(self):
        self.export_teams_instances()
        self.export_players()
        self.export_players_in_team()
        self.export_players_feed()



if __name__ == '__main__':
    ep = ExportPlayoff()
    print(ep)
