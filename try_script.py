from playoff_migration import PlayoffMigration, Games
from pprint import pprint

pm = PlayoffMigration()
original = Games.original
cloned = Games.cloned
scoped = Games.scoped

"""
# Erase design and data from cloned game
pm.delete_all_istances(cloned)
pm.delete_all_design(cloned)

# Migrate design and data to cloned game
pm.migrate_all_design(cloned)
pm.migrate_all_istances(cloned)

# Erase design and data from scoped game
pm.delete_all_istances(scoped)
pm.delete_all_design(scoped)

# Migrate scoped design and data to scoped game
pm.migrate_all_design_scoped(scoped)
pm.migrate_all_istances_scoped(scoped)
"""

# Print leaderboard
normal_board = pm.get_leaderboard(cloned, "tra_team_creativita")
scoped_board = pm.get_scoped_leaderboard(scoped, "tra_team_creativita")

print("\nNormal Board")
pprint(normal_board)
print("\nScoped Board")
pprint(scoped_board)




