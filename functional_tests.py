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

    def test_exists_original_game(self):
        """ esiste un gioco su playoff con id GameLabNoTargetV01 """
        self.assertTrue(self.pm.get_game_id(Games.original) == "GameLabNoTargetV01")

    def test_exists_cloned_game(self):
        """ esiste un gioco su playoff con id GameLabClonScoped """
        self.assertTrue(self.pm.get_game_id(Games.cloned) == "GameLabClonScoped")

    def test_cloned_game_contains_all_teams_from_original_game(self):
        """ il gioco nuovo contiene i team del gioco vecchio """
        self.assertTrue(self.pm.get_teams_by_id(Games.original) == self.pm.get_teams_by_id(Games.cloned))

    def test_cloned_game_contains_all_players_from_original_game(self):
        """ il gioco nuovo contiene tutti gli utenti del gioco vecchio """
        self.assertTrue(self.pm.get_players_by_id(Games.original) == self.pm.get_players_by_id(Games.cloned))

    def test_original_game_players_by_team_match_cloned_ones(self):
        """ i giocatori del gioco nuovo sono associati agli stessi team del gioco vecchio """
        self.test_cloned_game_contains_all_teams_from_original_game() # check if both games have same number of teams
        self.assertTrue(self.pm.get_players_by_teams(Games.original) == self.pm.get_players_by_teams(Games.cloned))

    # ==================
    # ogni giocatore del gioco nuovo ha un feed fatto delle stesse chiamate alle action a quello del gioco vecchio,
        # possono differire i timestamp degli eventi (del feed sono da considerare solo gli eventi con type='action')
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
