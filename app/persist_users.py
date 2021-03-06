

import db_interface
import csv_interface
import config

csv = csv_interface.Extract_CSV_Info(
    './data/Proof_homework.csv',
    ['User ID', 'IP', 'Geo', 'Industry', 'Company Size']
)
dsn = config.get_dsn(config.CONFIG)
db = db_interface.db_interface(dsn)

print db.add_users(csv.read_input_file())

