#!/usr/bin/python

import logging
import os
import config

from LanguageExplorer import app

if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG)
    app.run(debug=config.DEBUG, host='0.0.0.0', port=config.PORT)
