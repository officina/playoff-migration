from playoff_migration import Utility, PlayoffMigrationData, \
    PlayoffMigrationDesign

original = Utility.get_playoff_client(
    "ORIGINAL_CLIENT_ID",
    "ORIGINAL_CLIENT_SECRET",
    "ORIGINAL_HOSTNAME"
)

to_clone = Utility.get_playoff_client(
    "CLONED_CLIENT_ID",
    "CLONED_CLIENT_SECRET",
    "CLONED_HOSTNAME"
)

design_migrator = PlayoffMigrationDesign(original, to_clone)
data_migrator = PlayoffMigrationData(original, to_clone)

design_migrator.migrate_all_design()
data_migrator.migrate_all_data()
