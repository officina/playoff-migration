from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from playoff import Playoff
from playoff_migration import PlayoffMigration


class PlayoffMigrationTest(unittest.TestCase):
    
    pm:PlayoffMigration

    def setUp(self):

        self.pm = PlayoffMigration()
        self.browser = webdriver.Chrome()
    
    def tearDown(self):
        self.browser.quit()

    def test_exists_original_game(self):
        game_exist = self.pm.check_game("GameLabNoTargetV01")
        self.assertTrue(game_exist)

    def test_a_game_exists_with_id_gamelab_clone1(self):
        
        # esiste un gioco su playoff clone di id gamelab_target che si chiama gamelab_clone1
        game_exists = self.pm.check_game('mln_test')
        self.assertTrue(game_exists)
        

    def test_gamelab_clone1_contains_all_teams_from_gamelab_original(self):    
        # il gioco nuovo contiene i team del gioco vecchio
        
        self.fail("Not implemented!")

    # il gioco nuovo contiene tutti gli utenti del gioco vecchio
    # i giocatori del gioco nuovo sono associati agli stessi team del gioco vecchi
    # ogni giocatore del gioco nuovo ha un feed fatto delle stesse chiamate alle action a quello del gioco vecchio, possono differire i timestamp degli eventi (del feed sono da considerare solo gli eventi con type='action')
    # le leaderboard generate contengono degli zeri per i giocatori che non hanno fatto action
    # esiste un gioco su playoff clone di id gamelab_target che si chiama gamelab_clone2
    # il gioco nuovo contiene i team del gioco vecchio
    # il gioco nuovo contiene tutti gli utenti del gioco vecchio
    # i giocatori del gioco nuovo sono associati agli stessi team del gioco vecchi
    # ogni giocatore del gioco nuovo ha un feed fatto delle stesse chiamate alle action a quello del gioco vecchio, possono differire i timestamp degli eventi (del feed sono da considerare solo gli eventi con type='action')
    # le leaderboard generate contengono degli zeri per i giocatori che non hanno fatto action

if __name__ == '__main__':
    unittest.main(warnings='ignore')
    