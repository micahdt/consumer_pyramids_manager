import glob             #Package allows for all files in the directory to be collapsed into a list
import os               #Access environment variables
import pandas as pd     #Standard pandas package
import shutil           #Allows for optimized dataframe merge by row
import sys              #Access system indicators
import csv              #Enables exporting variable names to csv
from datetime import datetime
import time
from alive_progress import alive_bar
import inquirer
from itertools import chain
import random
from dateutil import relativedelta
from halo import Halo
from tkinter import Tk, filedialog
from pathlib import Path
import consumer_pyramids_manager.configure.configure as config
from consumer_pyramids_manager.configure.configure import bcolors
import json
from importlib import reload
from inquirer.themes import GreenPassion

global config_file
config_file = config.config_file

# ============================================================================================================
#                                               INITIALIZER
# ============================================================================================================
def initializer():
    data_directory = config.configure()[0]
    output_directory = config.configure()[1]
    os.chdir(sys.path[0])
    with open(config_file) as f:
        data = f.read()
    configuration = json.loads(data)
    if configuration["v_card"] == 0:
        advance_strategy = inquirer.confirm("Restore backed up selections for output and data directories?", default=False)
        if advance_strategy is True:
            os.chdir(sys.path[0])
            with open(config_file) as f:
                data = f.read()
            configuration = json.loads(data)
            configuration["output_directory"] = configuration["bkup_output_directory"]
            configuration["data_directory"] = configuration["bkup_data_directory"]
            with open(config_file, "w") as f:
                f.write(json.dumps(configuration))
            print(f"{bcolors.GREEN}Directories restored!{bcolors.END}")
            print("Data Directory: \n" + configuration["data_directory"])
            print("Output Directory: \n" + configuration["output_directory"]+"\n")
            config.configure()
            return

    advance_strategy = inquirer.confirm("Change the data directory?", default=True)
    while advance_strategy is True:
        root = Tk() # pointing root to Tk() to use it as Tk() in program.
        root.withdraw() # Hides small tkinter window.
        root.attributes('-topmost', True) # Opened windows will be active. above all windows despite of selection.
        data_directory = filedialog.askdirectory() 
        if not data_directory:
            print(f"{bcolors.WARNING}Invalid Selection:{bcolors.END} Data directory unchanged!\n")
            advance_strategy = inquirer.confirm("Reselect?", default=True)
            if advance_strategy is False:
                advance_strategy = False
                break
        else:
            print("Data directory changed: ")
            print(str(data_directory)+"\n")

            os.chdir(sys.path[0])
            with open(config_file) as f:
                data = f.read()
            configuration = json.loads(data)
            configuration["data_directory"] = data_directory
            with open(config_file, "w") as f:
                f.write(json.dumps(configuration))
            advance_strategy = False

    advance_strategy = inquirer.confirm("Change the output directory?", default=True)
    while advance_strategy is True:
        root = Tk() # pointing root to Tk() to use it as Tk() in program.
        root.withdraw() # Hides small tkinter window.
        root.attributes('-topmost', True) # Opened windows will be active. above all windows despite of selection.
        output_directory = filedialog.askdirectory() 
        if not output_directory:
            print(f"{bcolors.WARNING}Invalid Selection:{bcolors.END} Output directory unchanged!\n")
            advance_strategy = inquirer.confirm("Reselect?", default=True)
            if advance_strategy is False:
                advance_strategy = False
                break
        else:
            print("Output directory changed: ")
            print(str(output_directory)+"\n")

            os.chdir(sys.path[0])
            with open(config_file) as f:
                data = f.read()
            configuration = json.loads(data)
            configuration["output_directory"] = output_directory
            with open(config_file, "w") as f:
                f.write(json.dumps(configuration))
            advance_strategy = False

    advance_strategy = inquirer.confirm("Backup current selections for output and data directories?", default=False)
    if advance_strategy is True:
        os.chdir(sys.path[0])
        with open(config_file) as f:
            data = f.read()
        configuration = json.loads(data)
        configuration["bkup_output_directory"] = configuration["output_directory"]
        configuration["bkup_data_directory"] = configuration["data_directory"]
        with open(config_file, "w") as f:
            f.write(json.dumps(configuration))
        print(f"{bcolors.GREEN}Directories backed-up!{bcolors.END}")
        print("Data Directory: \n" + configuration["bkup_data_directory"])
        print("Output Directory: \n" + configuration["bkup_output_directory"]+"\n")

    os.chdir(sys.path[0])
    with open(config_file) as f:
        data = f.read()
    configuration = json.loads(data)
    configuration["v_card"] = 0
    with open(config_file, "w") as f:
        f.write(json.dumps(configuration))
    config.configure()  
    return