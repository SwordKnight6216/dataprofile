import os
from pathlib import Path

DEFAULT_SAMPLE_SIZE = -1
# AUTHOR = os.environ["USER"]
AUTHOR = 'Gordon Chen'
RANDOM_STATE = 0
MAX_STRING_SIZE = 15
LOG_FILE = Path(os.getenv("HOME"), "log", "dataprofile.log")
