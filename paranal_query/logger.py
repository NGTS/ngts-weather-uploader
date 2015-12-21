import logging
import logging.config
import json
import os

__all__ = ['logger']

BASE_DIR = os.path.realpath(
    os.path.dirname(__file__)
)
CONFIG_FILE_PATH = os.path.join(BASE_DIR, 'logging_config.json')

with open(CONFIG_FILE_PATH) as infile:
    config = json.load(infile)

logging.config.dictConfig(config)
logging.captureWarnings(True)

logger = logging.getLogger('paranal_weather')
