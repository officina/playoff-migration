from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from playoff import Playoff
from playoff_migration import PlayoffMigration
from playoff_migration import Games


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

    def test_exists_original_game(self):
        """ esiste un gioco su playoff con id GameLabNoTargetV01 """
        self.assertTrue(self.pm.get_game_id(Games.original) == "GameLabNoTargetV01")

    def test_exists_cloned_game(self):
        """ esiste un gioco su playoff con id GameLabClonScoped """
        self.assertTrue(self.pm.get_game_id(Games.cloned) == "GameLabClonScoped")

    def test_cloned_game_contains_all_teams_from_original_game(self):
        """ il gioco nuovo contiene i team del gioco vecchio """
        self.pm.migrate_teams()
        self.assertTrue(self.pm.get_teams_by_id(Games.original) == self.pm.get_teams_by_id(Games.cloned))

    def test_cloned_game_contains_all_players_from_original_game(self):
        """ il gioco nuovo contiene tutti gli utenti del gioco vecchio """
        self.pm.migrate_players()
        self.assertTrue(self.pm.get_players_by_id(Games.original) == self.pm.get_players_by_id(Games.cloned))

    def test_original_game_players_by_team_match_cloned_ones(self):
        """ i giocatori del gioco nuovo sono associati agli stessi team del gioco vecchio """
        self.test_cloned_game_contains_all_teams_from_original_game()  # check if both games have same number of teams
        self.pm.migrate_players_in_team()
        self.assertTrue(self.pm.get_players_by_teams(Games.original) == self.pm.get_players_by_teams(Games.cloned))

    # +++++++++++++
    # NON IMPLEMENTATI

    def test_original_game_player_feed_match_cloned_ones(self):
        """ ogni giocatore del gioco nuovo ha un feed fatto delle stesse chiamate alle action a quello del gioco
        vecchio, possono differire i timestamp degli eventi (del feed sono da considerare solo gli eventi
        con type='action')
        """
        self.test_cloned_game_contains_all_players_from_original_game()  # check if both games have same number of player

        players_by_id = self.pm.get_players_by_id(Games.original)  # at this point is not relevant what type of game
        # I choose form to retrieve players id
        condition = True

        for key in players_by_id:
            player_feed_original = self.pm.get_player_feed(Games.original, players_by_id.get(key))
            player_feed_cloned = self.pm.get_player_feed(Games.cloned, players_by_id.get(key))

            # filter by "event" = "action" (using list because get() method return a list of dict
            player_feed_original = list(filter(lambda x: x['event'] == 'action', player_feed_original))
            player_feed_cloned = list(filter(lambda x: x['event'] == 'action', player_feed_cloned))

            # TODO : check if for statement is useful, because we are checking only one feed at a time
            # remove timestamp because not important
            for item in player_feed_original:
                del item['timestamp']

            for item in player_feed_cloned:
                del item['timestamp']

            # if condition became False there isn't a reason to go on
            if not player_feed_original == player_feed_cloned:
                condition = False
                break

        self.assertTrue(condition)

    def test_leaderboard_has_players_with_score_0(self):
        """ le leaderboard generate contengono degli zeri per i giocatori che non hanno fatto action """
        # TODO : check functionality with Gamed.cloned argument (player_id issue)
        self.assertTrue(not self.pm.get_players_with_score_0(Games.original))

    # ==================
    # le leaderboard generate contengono degli zeri per i giocatori che non hanno fatto action
    # esiste un gioco su playoff clone di id gamelab_target che si chiama gamelab_clone2
    # il gioco nuovo contiene i team del gioco vecchio
    # il gioco nuovo contiene tutti gli utenti del gioco vecchio
    # i giocatori del gioco nuovo sono associati agli stessi team del gioco vecchi
    # ogni giocatore del gioco nuovo ha un feed fatto delle stesse chiamate alle action a quello del gioco vecchio, possono differire i timestamp degli eventi (del feed sono da considerare solo gli eventi con type='action')
    # le leaderboard generate contengono degli zeri per i giocatori che non hanno fatto action

"""
il blocco di codice successivo viene eseguito solo se è il modulo principale
quindi solo se eseguo "python playoff_migration.py"
"""
if __name__ == '__main__':
    unittest.main(warnings='ignore')
