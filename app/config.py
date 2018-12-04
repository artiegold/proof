import socket
import os

CONFIG = {
    'host': 'db',
    'port': 5433,
    'user': 'postgres',
    'password': 'postgres',
    'dbname': 'proof',
}

def get_dsn(config):
    return ' '.join(k + '=' + str(v) for k, v in config.iteritems())

def initialize_database(config):
    info = {
        '-h': config['host'],
        '-p': config['port'],
        '-U': config['user']
    }
    cmd = 'PGPASSWORD=' + config['password'] \
    + ' psql ' \
    + ' '.join((k + ' ' + str(info[k]) for k in ('-h', '-p', '-U'))) \
    + ' proof < ../db/create_tables.pgsql'
    os.system(cmd)

if __name__ == '__main__':
    initialize_database(CONFIG)
