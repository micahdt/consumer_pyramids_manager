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
#                                          PYRAMID BUILDER
# ============================================================================================================


def pyramid_builder():
    init_start = datetime.now()
    init_start_day = init_start.strftime("%Y%m%d")
    init_start_time = init_start.strftime("%H%M%S")
    data_directory = config.configure()[0]
    output_directory = config.configure()[1]

    while True:

        #Requesting input on desired values:
        print(f"""\n
    {bcolors.WARNING}NOTE:{bcolors.END} This program can only sample on either individuals or households.
    Opting not to sample observations can be memory and time intensive.\n""")
        newest_pyramid = sorted(os.
        listdir(Path(str(data_directory) + "/dataraw/income/monthly/individual/")))[-1]
        newest_pyramid = newest_pyramid[14:18]+"-"+newest_pyramid[18:20]
                
        questions = [
            inquirer.Confirm("sample_choice", message="Sample observations?", default=True),
            inquirer.List("sample_type", message="Sample on households or individuals", choices=["Households", "Individuals"], default="Neither",ignore=lambda x: x["sample_choice"] == False),
            inquirer.Text("number_of_individuals", message="Enter the desired sample size of individuals (int)", default="",ignore=lambda x: x["sample_type"] in ["Households","Neither"]),
            inquirer.Text("number_of_households", message="Enter the desired sample size of households (int)", default="",ignore=lambda x: x["sample_type"] in ["Individuals","Neither"]),
            inquirer.Text("start_date", message="Enter the desired start date of sample (YYYY-MM)", default="2014-01"),
            inquirer.Text("end_date", message="Enter the desired end date of sample (YYYY-MM)", default=newest_pyramid),
            inquirer.Text("seed_set", message="Enter the desired seed (int)", default=9231946),
            inquirer.Text("file_size", message="Enter the desired file chunk size (Gigabytes)", default=2.5),
            inquirer.Text("file_name", message="Enter the desired filename", default="sampled_pyramids"),
        ]
        user_input = inquirer.prompt(questions, theme=GreenPassion())

        advance_strategy = inquirer.confirm("Are the parameters correct?", default=True)
        if advance_strategy is False:
            return 2
        
        print("Checking for errors: ")
        #Setting variables based on inquirer requests:
        desired_dates = [list(user_input.values())[4], list(user_input.values())[5]]
        desired_individuals = list(user_input.values())[2]
        desired_households = list(user_input.values())[3]
        seed_set = list(user_input.values())[6]
        desired_chunk_size = list(user_input.values())[7]
        desired_file_name = str(list(user_input.values())[8])

        #Setting the random seed
        random.seed(seed_set)

        #Error checking the sampling selections:
        if (desired_individuals == '' and desired_households == ''):
            print(f"\n{bcolors.WARNING}WARNING:{bcolors.END} No sampling selected.\nThis may be data and time intensive.\n")
            advance_strategy = inquirer.confirm("Do you want to continue?", default=True)
            if advance_strategy is False:
                return 0
        elif (desired_households != '' and desired_individuals != ''):
            input(f"{bcolors.WARNING}WARNING:{bcolors.END} Must sample on households or individuals! \nPress enter to continue: ")
            return 0
        if (desired_households != ''):
            try:
                desired_households = int(desired_households)
                if isinstance(desired_households, int):
                    if (desired_households <= 0):
                            input(f"{bcolors.WARNING}WARNING:{bcolors.END} Invalid household sample size selected!")
                            return 0
                else:
                    input(f"{bcolors.WARNING}WARNING:{bcolors.END} Household sample size must be an integer! \nPress enter to continue: ")
                    return 0
            except:
                input(f"{bcolors.WARNING}WARNING:{bcolors.END} Household sample size must be an integer! \nPress enter to continue: ")
                return 0
        elif(desired_individuals != ''):
            try:
                desired_individuals = int(desired_individuals)
                if isinstance(desired_individuals, int):
                    if (desired_individuals <= 0):
                        input(f"{bcolors.WARNING}WARNING:{bcolors.END} Invalid individual sample size selected! \nPress enter to continue: ")
                        return 0
                else:
                    input(f"{bcolors.WARNING}WARNING:{bcolors.END} Individual sample size must be an integer! \nPress enter to continue: ")
                    return 0
            except:
                input(f"{bcolors.WARNING}WARNING:{bcolors.END} Individual sample size must be an integer! \nPress enter to continue: ")
                return 0

        #Error checking the date selections:
        if isinstance(desired_dates[0], str) & isinstance(desired_dates[1], str):
            try:
                time.strptime(desired_dates[0], "%Y-%m")
            except ValueError:
                input(f"{bcolors.WARNING}WARNING:{bcolors.END} Date selection must be a valid string! \nPress enter to continue:")
                return 0
            try:
                time.strptime(desired_dates[1], "%Y-%m")
            except ValueError:
                input(f"{bcolors.WARNING}WARNING:{bcolors.END} Date selection must be a valid string! \nPress enter to continue: ")
                return 0
            if (time.strptime(desired_dates[0], "%Y-%m") < time.strptime('2014-01', "%Y-%m")):
                print(f"{bcolors.WARNING}WARNING:{bcolors.END} Earliest date collected 2014-01\n")
                advance_strategy = inquirer.confirm("Do you want to continue? ", default=True)
                while advance_strategy is False:
                    return 0
                desired_dates[0] = time.strptime('2014-01', "%Y-%m")
            if (time.strptime(desired_dates[0], "%Y-%m") > time.strptime(desired_dates[1], "%Y-%m")):
                input(f"{bcolors.WARNING}WARNING:{bcolors.END} Begin date later than end date! \nPress enter to continue: ")
                return 0
        else:
            input(f"{bcolors.WARNING}WARNING:{bcolors.END} Date selection must be a valid string! \nPress enter to continue: ")
            return 0

        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')
        print("Checking for errors: Done!")

        #Pulling identifiers
        with Halo(text="Pulling idenitifiers: ", spinner='dots', color = 'magenta', placement = 'right'):
            #Creating month index for loops based on desired dates:
            delta = relativedelta.relativedelta(datetime.strptime(desired_dates[1], "%Y-%m"), datetime.strptime(desired_dates[0], "%Y-%m"))
            desired_months = delta.months + (delta.years * 12)

            #Importing the identifiers from all the available waves (Household ID, Individual ID, Member ID)
            identifiers = pd.read_csv(Path(str(data_directory) + "/codebook/HH_INDIV_identifiers.csv"))
            #Converting Month column into  bca datetime object
            identifiers['MONTH'] = pd.to_datetime(identifiers['MONTH'])
            #Creating list of selected dates after error checking
            dates = pd.date_range(desired_dates[0],desired_dates[1], freq='MS').strftime("%Y-%m").tolist()
            #Selecting Identifiers of Selected Dates (Defaults to all dates)
            identifiers = identifiers.loc[(identifiers['MONTH'] >= desired_dates[0]) & (identifiers['MONTH'] <= desired_dates[1])]

            #Pulling Individual IDs for individual level sampling
            individual_ids = sorted([*set(identifiers['INDIV_ID'].tolist())])
            #Pulling Household IDs for household level sampling
            household_ids = sorted([*set(identifiers['HH_ID'].tolist())])

            sys.stdout.write('\x1b[2K')
            print("\rPulling identifiers: Done!")

        print("Sampling identifiers: ")
        #Sampling households or individuals:
        if (desired_households != ''):
            try:
                households_sampled = sorted(random.sample(household_ids,desired_households))
            except ValueError as ve:
                #sys.stdout.write("\033[F")
                #print(f"Sampling identifiers: {bcolors.WARNING}Invalid Sample Size!{bcolors.END}")
                print(f"\n{bcolors.WARNING}WARNING:{bcolors.END} Invalid sample size.\nDesired sample size is larger than population.\n")
                return 0
            identifiers_sampled = identifiers[identifiers['HH_ID'].isin(households_sampled)]
        elif(desired_individuals != ''):
            try:
                individuals_sampled = sorted(random.sample(individual_ids, desired_individuals))
            except ValueError as ve:
                #sys.stdout.write("\033[F")
                #print(f"Sampling identifiers: {bcolors.WARNING}Invalid Sample Size!{bcolors.END}")
                print(f"\n{bcolors.WARNING}WARNING:{bcolors.END} Invalid sample size.\nDesired sample size is larger than population.\n")
                return 0
            identifiers_sampled = identifiers[identifiers['INDIV_ID'].isin(individuals_sampled)]
        else:
            identifiers_sampled = identifiers

        sys.stdout.write('\x1b[2K')
        print("\rSampling idenitifiers: Done!")



        with Halo(text = "Pulling selected variables: ", spinner='dots', color = 'magenta', placement = 'right'):
        #Importing the variables of interest as selected by the user 
            xls = pd.ExcelFile(Path(str(data_directory) + "/codebook/vars_selected.xlsx"))
            vars_aspirational_quarterly = tuple(list(chain(*((pd.read_excel(xls, 'aspirational_quarterly',header=None)).to_numpy()).tolist())))
            vars_people_quarterly = tuple(list(chain(*((pd.read_excel(xls, 'people_quarterly',header=None)).to_numpy()).tolist())))
            vars_consumption_quarterly = tuple(list(chain(*((pd.read_excel(xls, 'consumption_quarterly',header=None)).to_numpy()).tolist())))
            vars_consumption_monthly = tuple(list(chain(*((pd.read_excel(xls, 'consumption_monthly',header=None)).to_numpy()).tolist())))
            vars_income_monthly_household = tuple(list(chain(*((pd.read_excel(xls, 'income_monthly_household',header=None)).to_numpy()).tolist())))
            vars_income_monthly_individual = tuple(list(chain(*((pd.read_excel(xls, 'income_monthly_individual',header=None)).to_numpy()).tolist())))
            sys.stdout.write('\x1b[2K')
            print("\rPulling selected variables: Done!")


        with Halo(text = "Sampling and merging across waves: ", spinner='dots', color='magenta', placement = 'right'):
            #Import the raw data available for sampling:
            income_monthly_individual_files = sorted(glob.glob(os.path.join(Path(str(data_directory) + "/dataraw/income/monthly/individual/"), "*.csv")))
            income_monthly_household_files = sorted(glob.glob(os.path.join(Path(str(data_directory) + "/dataraw/income/monthly/household/"), "*.csv")))
            consumption_monthly_household_files  = sorted(glob.glob(os.path.join(Path(str(data_directory) + "/dataraw/consumption/monthly/"), "*.csv")))
            consumption_quarterly_household_files = sorted(glob.glob(os.path.join(Path(str(data_directory) + "/dataraw/consumption/quarterly/"), "*.csv")))
            aspirational_quarterly_household_files = sorted(glob.glob(os.path.join(Path(str(data_directory) + "/dataraw/aspirational/quarterly/"), "*.csv")))
            people_quarterly_individual_files = sorted(glob.glob(os.path.join(Path(str(data_directory) + "/dataraw/people/quarterly/"), "*.csv")))

            #Creating the tempfiles folder for use in merging:
            #Setting output folder
            tempfiles = Path(str(output_directory) + "/tempfiles_"+init_start_day+"_"+init_start_time+"/")
            os.mkdir(tempfiles)
            os.chdir(tempfiles)
            sys.stdout.write('\x1b[2K')
            print("\rSampling and merging across waves: ")

        #Merge each month across the monthly files with appropriate quarterly file
        with alive_bar(len(["M"]*(desired_months+1))) as bar:
            for monthly_index in range(0,desired_months+1):
                #Declaring the quarterly file index for merging
                quarterly_index = monthly_index//4

                #Importing the individual income iteration
                income_monthly_individual_iteration = pd.read_csv(income_monthly_individual_files[monthly_index], usecols=lambda c: c in set(vars_income_monthly_individual),low_memory=False)#.add_suffix('_ii')
                income_monthly_individual_iteration = income_monthly_individual_iteration[income_monthly_individual_iteration['INDIV_ID'].isin(identifiers_sampled['INDIV_ID'])]

                #Importing the household income iteration
                income_monthly_household_iteration = pd.read_csv(income_monthly_household_files[monthly_index], usecols=lambda c: c in set(vars_income_monthly_household),low_memory=False)#.add_suffix('_ih')
                income_monthly_household_iteration = income_monthly_household_iteration[income_monthly_household_iteration['HH_ID'].isin(identifiers_sampled['HH_ID'])]

                #Importing the household consumption iteration
                consumption_monthly_household_iteration = pd.read_csv(consumption_monthly_household_files[monthly_index], usecols=lambda c: c in set(vars_consumption_monthly),low_memory=False)#.add_suffix('_cm')
                consumption_monthly_household_iteration = consumption_monthly_household_iteration[consumption_monthly_household_iteration['HH_ID'].isin(identifiers_sampled['HH_ID'])]

                #Importing the weekly household consumption iteration
                consumption_quarterly_household_iteration = pd.read_csv(consumption_quarterly_household_files[quarterly_index], usecols=lambda c: c in set(vars_consumption_quarterly),low_memory=False)#.add_suffix('_cw')
                consumption_quarterly_household_iteration = consumption_quarterly_household_iteration[consumption_quarterly_household_iteration['HH_ID'].isin(identifiers_sampled['HH_ID'])]

                #Importing the people iteration
                people_quarterly_individual_iteration = pd.read_csv(people_quarterly_individual_files[quarterly_index], usecols=lambda c: c in set(vars_people_quarterly),low_memory=False)#.add_suffix('_pq')
                people_quarterly_individual_iteration = people_quarterly_individual_iteration[people_quarterly_individual_iteration['INDIV_ID'].isin(identifiers_sampled['INDIV_ID'])]

                #Importing the aspirational iteration
                aspirational_quarterly_household_iteration = pd.read_csv(aspirational_quarterly_household_files[quarterly_index], usecols=lambda c: c in set(vars_aspirational_quarterly),low_memory=False)#.add_suffix('_aq')
                aspirational_quarterly_household_iteration = aspirational_quarterly_household_iteration[aspirational_quarterly_household_iteration['HH_ID'].isin(identifiers_sampled['HH_ID'])]
                
                #Merging individual level iterations:
                merged_individual = pd.merge(income_monthly_individual_iteration, people_quarterly_individual_iteration, on="INDIV_ID", how = 'outer', suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')

                #Merging household level iterations
                merged_household = pd.merge(income_monthly_household_iteration, consumption_monthly_household_iteration, on="HH_ID", how = 'outer', suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')
                merged_household = pd.merge(merged_household, consumption_quarterly_household_iteration, on="HH_ID", how = 'outer', suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')
                merged_household = pd.merge(merged_household, aspirational_quarterly_household_iteration, on="HH_ID", how = 'outer', suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')
                merged_iteration = pd.merge(merged_individual, merged_household, on="HH_ID", how = 'outer', suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')

                #Exporting the completed merged iteration
                merged_iteration.to_csv('merged_part_'+str(monthly_index+1)+'.csv', index=False)
                bar()
        
        #Grabbing the sampled merged tempfiles
        joined_files = glob.glob(os.path.join(tempfiles, "*.csv"))
        output_directory = Path(str(output_directory) + "/merged_" + init_start_day + "_" + init_start_time)
        os.mkdir(output_directory)
        #Declaring the output file name
        target_file_name = Path(str(output_directory) +"_"+ desired_file_name + ".csv")

        print("Merging final panel...")
        #Merging all of the tempfiles
        observations = []
        with alive_bar(len(joined_files)) as bar:
            for filename in joined_files:
                file_iteration = pd.read_csv(filename, index_col=None, header=0,low_memory=False)
                observations.append(file_iteration)
                bar()
        frame = pd.concat(observations, axis=0, ignore_index=True)
        frame.to_csv(target_file_name, index=False)

        #Creating log text file that says the start date and time as well as the sampling characteristics.
        text_file = open((Path(str(output_directory) + "_" + desired_file_name + "_parameters_" + ".txt")), "w")
        n = text_file.write("Data sampled on: " + str(init_start_day) + " at " + str(init_start_time) + "\nMonths sampled: " + str(desired_dates[0]) + " through " + str(desired_dates[1]) + "\nHouseholds sampled: " + str(desired_households) + "\nIndividuals sampled: " + str(desired_individuals) + "\nSeed: " + str(seed_set))
        text_file.close()

        print("Breaking file into desired chunk size...")
        #Breaking apart final panel into desired size:
        with open(target_file_name, "r") as file:
            number_of_lines = len(file.readlines())
        #Capture total file size and convert to gigabytes
        total_file_size = float(os.path.getsize(target_file_name)/1000000000)
        list(user_input.values())[4]
        list(user_input.values())[4]

        if total_file_size > float(desired_chunk_size):
            desired_chunk_lines = int((1/(float(total_file_size)/float(desired_chunk_size)))*float(number_of_lines))
            part_index = 1
            with alive_bar(len(["M"]*(int(float(desired_chunk_lines)/float(number_of_lines))))) as bar:
                for i,chunk in enumerate(pd.read_csv(target_file_name, chunksize=desired_chunk_lines,low_memory=False)):
                    chunk.to_csv(Path(str(output_directory) +"/"+ desired_file_name+"_part_"+str(part_index)+".csv"), index=False)
                    part_index = part_index+1
                bar()
            print("Chunks saved to:\n" + str(Path(str(output_directory) + "/" + desired_file_name+"_part_#.csv")))
            print("\nNOTE: The full merged panel is: " + str(total_file_size) + " Gigabytes.")
            correct = inquirer.confirm("Do you wish to delete the full merged panel?", default=False)
            if correct is True:
                os.remove(target_file_name)
                print("Full merged panel deleted.")
        else:
            shutil.rmtree(str(Path(str(output_directory))))
            print(f"{bcolors.WARNING}Desired chunk size larger than output file.{bcolors.END}")
            print("Panel saved to:\n" + str(target_file_name))

        #Cleaning up tempfiles
        shutil.rmtree(tempfiles)

        input(f"\n{bcolors.GREEN}Construction Complete.{bcolors.END} Press enter to return to the construction menu:")
        return 1