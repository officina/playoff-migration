from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from playoff import Playoff
from playoff_migration import PlayoffMigration
from playoff_migration import Games
from pprint import pprint


class PlayoffMigrationTest(unittest.TestCase):

    pm: PlayoffMigration

    def setUp(self):

        self.pm = PlayoffMigration()
        # self.browser = webdriver.Chrome(r"C:\Users\MisterWeeMan\Desktop\University\Stage\chromedriver.exe")
    
    def tearDown(self):
        # self.browser.quit()
        pass

    # +++++++++++++
    # IMPLEMENTATI

    def test0_exists_original_game(self):
        """ esiste un gioco su playoff con id GameLabNoTargetV01 """
        self.assertTrue(self.pm.get_game_id(Games.original) == "GameLabNoTargetV01")

    def test0_exists_cloned_game(self):
        """ esiste un gioco su playoff con id GameLabClonScoped3 """
        self.assertTrue(self.pm.get_game_id(Games.cloned) == "GameLabClonScoped3")

    def test1_cloned_game_contains_all_teams_from_original_game(self):
        # il gioco nuovo contiene i team del gioco vecchio
        self.pm.migrate_teams_instances()
        self.assertTrue(self.pm.get_teams_by_id(Games.original) == self.pm.get_teams_by_id(Games.cloned))

    def test2_cloned_game_contains_all_players_from_original_game(self):
        # il gioco nuovo contiene tutti gli utenti del gioco vecchio
        self.pm.migrate_players()
        self.assertTrue(self.pm.get_players_by_id(Games.original) == self.pm.get_players_by_id(Games.cloned))

    def test3_original_game_players_by_team_match_cloned_ones(self):
        # i giocatori del gioco nuovo sono associati agli stessi team del gioco vecchio
        self.test1_cloned_game_contains_all_teams_from_original_game()  # check if both games have same number of teams
        self.pm.migrate_players_in_team()
        self.assertTrue(self.pm.get_players_by_teams(Games.original) == self.pm.get_players_by_teams(Games.cloned))

    def test4_players_feed(self):
        # ogni giocatore del gioco nuovo ha un feed fatto delle stesse chiamate alle action a quello del gioco
        # vecchio, possono differire i timestamp degli eventi (del feed sono da considerare solo gli eventi
        # con type='action')
        self.pm.migrate_players_feed()
        players_by_id = self.pm.get_players_by_id(Games.original)  # at this point is not relevant what type of game
        # I choose form to retrieve players id
        condition = True

        for key in players_by_id:
            player_feed_original = self.pm.get_player_feed(Games.original, players_by_id.get(key))
            player_feed_cloned = self.pm.get_player_feed(Games.cloned, players_by_id.get(key))

            # filter by "event" = "action" (using list because get() method return a list of dict
            player_feed_original = list(filter(lambda x: x['event'] == 'action', player_feed_original))
            player_feed_cloned = list(filter(lambda x: x['event'] == 'action', player_feed_cloned))

            # remove info because not useful
            for item in player_feed_original:
                del item['timestamp']
                del item['id']
                if 'changes' in item:
                    del item['changes']

            for item in player_feed_cloned:
                del item['timestamp']
                del item['id']
                if 'changes' in item:
                    del item['changes']

            # if condition became False there isn't a reason to go on
            if not player_feed_original == player_feed_cloned:
                pprint(player_feed_original)
                pprint(player_feed_cloned)
                condition = False
                break

        self.assertTrue(condition)

    def test5_leaderboards_containing_scores_0(self):
        """ le leaderboard generate contengono degli zeri per i giocatori che non hanno fatto action """
        self.assertTrue(not self.pm.get_players_with_score_0(Games.cloned))

    # ++++++++++++++++
    # NON IMPLEMENTATI

    # ==================
    # esiste un gioco su playoff clone di id gamelab_target che si chiama gamelab_clone2
    # il gioco nuovo contiene i team del gioco vecchio
    # il gioco nuovo contiene tutti gli utenti del gioco vecchio
    # i giocatori del gioco nuovo sono associati agli stessi team del gioco vecchi
    # ogni giocatore del gioco nuovo ha un feed fatto delle stesse chiamate alle action a quello del gioco vecchio,
        # possono differire i timestamp degli eventi (del feed sono da considerare solo gli eventi con type='action')
    # le leaderboard generate contengono degli zeri per i giocatori che non hanno fatto action


if __name__ == '__main__':
    unittest.main(warnings='ignore')
