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

    # esiste un gioco su playoff con id GameLabNoTargetV01
    def test_exists_original_game(self):
        self.assertTrue(self.pm.get_game_id(Games.original) == "GameLabNoTargetV01")

    # esiste un gioco su playoff con id GameLabClonScoped
    def test_exists_cloned_game(self):
        self.assertTrue(self.pm.get_game_id(Games.cloned) == "GameLabClonScoped")

    # il gioco nuovo contiene i team del gioco vecchio
    def test_cloned_game_contains_all_teams_from_original_game(self):
        self.assertTrue(self.pm.get_teams(Games.original) == self.pm.get_teams(Games.cloned))


#=======
    def test_gamelab_clone1_contains_all_players_from_gamelab_original(self):
        # il gioco nuovo contiene tutti gli utenti del gioco vecchio
        player_equals = self.pm.check_all_players()
        self.assertTrue(player_equals)

    def test_gamelab_clone1_team_players_match_team_players_gamelab_original(self):
        # i giocatori del gioco nuovo sono associati agli stessi team del gioco vecchio
        team_players = self.pm.team_players_match()
        self.assertTrue(team_players)

    # ogni giocatore del gioco nuovo ha un feed fatto delle stesse chiamate alle action a quello del gioco vecchio, possono differire i timestamp degli eventi (del feed sono da considerare solo gli eventi con type='action')
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
