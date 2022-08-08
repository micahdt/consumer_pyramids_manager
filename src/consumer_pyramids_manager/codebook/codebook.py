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
#                                          INDIVIDUAL ID GENERATOR
# ============================================================================================================


def id_generator():
    data_directory = config.configure()[0]
    output_directory = config.configure()[1]
    for pyramid in ["people_quarterly", "income_monthly_individual"]:
        if pyramid == "people_quarterly":
            data_dir = Path(str(data_directory) + "/dataraw/people/quarterly/")
            print("Generating Individual IDs in Quarterly People Files:")
        elif pyramid == "income_monthly_individual":
            data_dir = Path(str(data_directory) + "/dataraw/income/monthly/individual/")
            print("Generating Individual IDs in Monthly Household Income Files:")
        #Generating a unique Individual ID column based on the Household ID and Member ID
        #Changing directory to data directory
        os.chdir(data_dir)
        #Creates a singular list of raw csv files in data directory
        joined_files = os.path.join(data_dir, "*.csv")
        joined_files = glob.glob(joined_files)
        #Loops through each file in the directory
        with alive_bar(len(joined_files)) as bar:
            for file in joined_files:
                #Checks if the INDIV_ID variable has been generated already in this iteration
                id_check = pd.read_csv(file, usecols=lambda c: c in {'INDIV_ID'})
                #If the variable is not present in the iteration
                if id_check.empty:
                #Load the iteration
                    iteration = pd.read_csv(file)
                    #Format Member ID as a two digit str with padded zeros
                    iteration["MEM_ID"] = (iteration["MEM_ID"].astype(str)).str.zfill(2)
                    #Concatenate the padded Member ID with the Household ID as a string
                    iteration["INDIV_ID"] = iteration["HH_ID"].astype(str) + iteration["MEM_ID"].astype(str)
                    #Saving the original data with new individual ID column
                    iteration.to_csv(file, index=False)
                bar()
    return



# ============================================================================================================
#                                       IDENTIFIERS CAPTURE FUNCTION
# ============================================================================================================


def identifiers_capture():
    data_directory = config.configure()[0]
    output_directory = config.configure()[1]
    print("Collecting Identifiers:")# From Each Monthly Individual Income File: ")
    #Creates a singular list of raw csv files in data directory
    joined_files = glob.glob(os.path.join(Path(str(data_directory)+"/dataraw/income/monthly/individual/"), "*.csv"))

    observations = []
    with alive_bar(len(joined_files)) as bar:
        for filename in joined_files:
            file_iteration = pd.read_csv(filename, usecols=lambda c: c in {'INDIV_ID', 'HH_ID', 'MONTH'},low_memory=False, index_col=None, header=0)
            observations.append(file_iteration)
            bar()
    
    with Halo(text = "Saving Identifiers: ", spinner='dots', color='magenta', placement = 'right'):
        frame = pd.concat(observations, axis=0, ignore_index=True)
        frame.to_csv(Path(str(data_directory) + "/codebook/HH_INDIV_identifiers.csv"), index=False)
    sys.stdout.write('\x1b[2K')
    print("Saving Identifiers: Done!")




# ============================================================================================================
#                                          VARIABLES CAPTURE
# ============================================================================================================


def variables_capture():
    data_directory = config.configure()[0]
    output_directory = config.configure()[1]
    pyramids = ["aspirational_quarterly", "people_quarterly", "consumption_quarterly", "consumption_monthly" , "income_monthly_household", "income_monthly_individual"]
    #Beginning the capture of varaible names
    with pd.ExcelWriter(Path(str(data_directory) + "/codebook/vars_all.xlsx")) as writer:  
        for pyramid in pyramids:
            #Creating pointer to data directoy using environment variable
            if pyramid == "aspirational_quarterly":
                data_dir = str(Path(str(data_directory) + "/dataraw/aspirational/quarterly/"))
                print("Collecting Variables from the Quarterly Aspirational Pyramids:")
            elif pyramid == "consumption_quarterly":
                data_dir = str(Path(str(data_directory) + "/dataraw/consumption/quarterly/"))
                print("Collecting Variables from the Quarterly Household Consumption Pyramids:")
            elif pyramid == "consumption_monthly":
                data_dir = str(Path(str(data_directory) + "/dataraw/consumption/monthly/"))
                print("Collecting Variables from the Monthly Household Consumption Pyramids:")
            elif pyramid == "income_monthly_household":
                data_dir = str(Path(str(data_directory) + "/dataraw/income/monthly/household/"))
                print("Collecting Variables from the Monthly Household Income Pyramids:")
            elif pyramid == "people_quarterly":
                data_dir = str(Path(str(data_directory) + "/dataraw/people/quarterly/"))
                print("Collecting Variables from the Quarterly People Pyramids:")
            elif pyramid == "income_monthly_individual":
                data_dir = str(Path(str(data_directory) + "/dataraw/income/monthly/individual/"))
                print("Collecting Variables from the Monthly Individual Income Pyramids:")
                
            #Changing directory to data directory
            os.chdir(data_dir)

            #Creates a singular list of raw csv files in data directory
            joined_files = sorted(glob.glob(os.path.join(data_dir, "*.csv")))

            #Capturing variable names from each file and appending to list
            variable_names = []
            with alive_bar(len(joined_files)) as bar:
                for file in joined_files:
                    with open(file, 'r') as infile:
                        reader = csv.DictReader(infile)
                        fieldnames = reader.fieldnames
                    for item in fieldnames:
                        variable_names.append(item) if item not in variable_names else None
                    bar()
            df = pd.DataFrame(sorted([*set(variable_names)]))
            with Halo(text="Saving:", spinner='dots', color = 'magenta', placement = 'right'):
                df.to_excel(writer, sheet_name=pyramid, header=False, index=False)
            sys.stdout.write("\033[F")
    os.chdir(str(Path(str(data_directory) + "/codebook/")))
    shutil.copyfile("vars_all.xlsx", "vars_selected.xlsx")
