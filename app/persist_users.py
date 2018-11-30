#! /usr/bin/env python

import db_interface
import csv_interface

csv = csv_interface.Extract_CSV_Info(
    '../data/input/Proof_homework.csv',
    ['User ID', 'IP', 'Geo', 'Industry', 'Company Size']
)

db = db_interface.db_interface('')

print db.add_users(csv.read_input_file())

