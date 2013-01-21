#!/usr/bin/python

import argparse
import logging
import os

import config

from LanguageExplorer import app
from LanguageExplorer.model import connect_db, db

if __name__ == '__main__':
    # Set up commandline arguments
    parser = argparse.ArgumentParser('Flags for running the server.')
    parser.add_argument('--create_db', action='store_true', default=False, \
                        help='Create tables in DB.')
    args = parser.parse_args()
    # Connect to DB. Create tables only when --create_db is specified.
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_CONFIG
    connect_db(app)
    if args.create_db:
      db.create_all(app=app)
    # Run server until it is killed or interrupted by ^C.
    app.logger.setLevel(logging.DEBUG)
    app.run(debug=config.DEBUG, host='0.0.0.0', port=config.PORT)
