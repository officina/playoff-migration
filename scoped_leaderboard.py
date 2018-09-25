from pprint import pprint

from refactor_playoff_migration import ParameterException, \
    PlayoffMigrationDesign, PlayoffMigrationData, Utility


class ScopedUtility(Utility):
    """Class that define methods or constants useful for the other class"""

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

    @staticmethod
    def get_globale_scopes(player_id, action_id):
        """Return a list with scopes for a player in "globale" team

        :param str player_id: player id to add in scopes
        :param str action_id: action id used to add a scope
        :raise: ParameterException: when a parameters is empty
        """
        if not player_id or not action_id:
            raise ParameterException("Parameters can't be empty")

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
                    "id": ScopedUtility.ACTION_LEADERBOARD_PARSER[action_id],
                    "entity_id": player_id
                }]

    @staticmethod
    def get_lab_somma_scopes(player_id):
        """Return a list with scopes for a player in "laboratorio_somma" team

        :param player_id: player id to add in scopes
        :raise: ParameterException: when parameter is empty
        """
        if not player_id:
            raise ParameterException("Parameter can't be empty")

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


class ScopedLeaderboard(PlayoffMigrationDesign, PlayoffMigrationData):
    """Class that trasform normal leaderboard in scoped one in the process of
    migrating it in another game
    """

    def __init__(self):
        # super().__init__()
        PlayoffMigrationDesign.__init__(self)
        PlayoffMigrationData.__init__(self)

    def migrate_leaderboards_design(self):
        """Migrate scoped leaderboards design"""
        self.logger.info("migrating scoped leaderboards design")

        leaderboards_id = self.design_getter.get_leaderboards_design()

        self.design_destroyer.delete_leaderboards_design()

        for leaderboard in leaderboards_id:
            self.logger.debug("migrating scoped leaderboard design " +
                              leaderboard['id'])

            single_design = self.design_getter.get_single_leaderboard_design(
                leaderboard['id'])

            data = {
                "id": single_design['id'],
                "name": single_design['name'],
                "entity_type": single_design['entity_type'],
                "scope": {"type": "custom"},
                "metric": single_design['metric']
            }

            self.design_creator.create_leaderboard_design(data)

        self.logger.info("scoped leaderboards design migration finished")

    def migrate_player_feed(self, player_id, player_feed):
        """Migrate scoped player feed

        :param dict player_id: player id in dict format
        :param dict player_feed: player feed
        :raise ParameterException: if a parameter is empty
        """
        ScopedUtility.raise_empty_parameter_exception([player_id, player_feed])

        feed_count = str(len(player_feed))
        index = 0

        self.logger.debug("migrating " + feed_count + " scoped feed of player "
                          + player_id['player_id'])

        player_data = self.data_getter.get_player_profile(
            player_id['player_id'])
        player_teams = player_data['teams']

        for feed in player_feed:

            if feed["event"] == "action":
                action_id = feed['action']['id']
                variables = feed['action']['vars']
                scopes = {}

                for team in player_teams:
                    if team["id"] == "globale":
                        scopes = ScopedUtility.get_globale_scopes(
                            player_id['player_id'], action_id)
                        break
                    elif team["id"] == "community_somma":
                        scopes = ScopedUtility.get_lab_somma_scopes(
                            player_id['player_id'])
                        break

                if not scopes:
                    scopes = feed['scopes']

                data = {
                    "variables": variables,
                    "scopes": scopes
                }

                self.data_creator.take_action(action_id, player_id, data)

                index += 1
                self.logger.debug("migrated " + index + " of " + feed_count +
                                  " scoped feed")

        self.logger.debug("scoped feed migration finished")
