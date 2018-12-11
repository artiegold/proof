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
