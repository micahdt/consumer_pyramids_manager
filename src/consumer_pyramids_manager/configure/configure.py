import os
from pathlib import Path
import json
import sys

global config_file
config_file = "config.txt" if os.name == 'nt' else ".config.txt"

def configure():
    os.chdir(sys.path[0])
    if os.path.exists(config_file) == True:
        os.chdir(sys.path[0])
        with open(config_file) as f:
            data = f.read()
        configuration = json.loads(data)
        data_directory = configuration["data_directory"]
        output_directory = configuration["output_directory"]
        return data_directory, output_directory



class bcolors:
    RED = '\u001b[31;1m'
    END = '\u001b[0m'
    ORANGE = '\u001b[38;5;208m'
    WARNING = '\u001b[38;5;226m'
    GREEN = '\u001b[38;5;10m'