import pyfiglet
import os               #Access environment variables
import pandas as pd     #Standard pandas package
import shutil           #Allows for optimized dataframe merge by row
import time
import inquirer
from itertools import chain
from inquirer.themes import GreenPassion
from simple_term_menu import TerminalMenu
from pathlib import Path
import json
import sys
import consumer_pyramids_manager.configure.configure as config
from consumer_pyramids_manager.configure.configure import bcolors
from consumer_pyramids_manager.codebook.codebook import id_generator
from consumer_pyramids_manager.codebook.codebook import identifiers_capture 
from consumer_pyramids_manager.codebook.codebook import variables_capture
from consumer_pyramids_manager.initializer.initializer import initializer
from consumer_pyramids_manager.builder.builder import pyramid_builder


# ===================================================================
#                           INITIAL CONDITIONS
# ===================================================================
#welcome_banner = pyfiglet.figlet_format("CONSUMER PYRAMIDS MANAGER", justify = "center", font = "small")
welcome_banner = ("""
                   ___                                 
                  / __|___ _ _  ____  _ _ __  ___ _ _  
                 | (__/ _ \ ' \(_-< || | '  \/ -_) '_| 
                  \___\___/_||_/__/\_,_|_|_|_\___|_|  
                  ___                     _    _
                 | _ \_  _ _ _ __ _ _ __ (_)__| |___   
                 |  _/ || | '_/ _` | '  \| / _` (_-<   
                 |_|  \_, |_| \__,_|_|_|_|_\__,_/__/   
                     |__/  
                  __  __                             
                 |  \/  |__ _ _ _  __ _ __ _ ___ _ _   
                 | |\/| / _` | ' \/ _` / _` / -_) '_|  
                 |_|  |_\__,_|_||_\__,_\__, \___|_|    
                                       |___/           
""")
initializer_banner = pyfiglet.figlet_format("INITIALIZER", justify = "center", font = "small")
help_banner = pyfiglet.figlet_format("HELP MENU", justify = "center", font = "small")
update_codebook_banner = pyfiglet.figlet_format("UPDATE CODEBOOK", justify = "center", font = "small")
variable_selector_banner = pyfiglet.figlet_format("VARIABLE SELECTOR", justify = "center", font = "small")
pyramid_builder_banner = pyfiglet.figlet_format("PYRAMID BUILDER\n", justify = "center", font = "small")

global config_file
config_file = "config.txt" if os.name == 'nt' else ".config.txt"
global data_directory
data_directory = config.configure()[0]
global output_directory
output_directory = config.configure()[1]

def clear_prompt():
    if os.name == 'nt':
        _=os.system("cls")
    else:
        _=os.system("clear")  

def init():
    os.chdir(sys.path[0])
    #config_file = "config.txt" if os.name == 'nt' else ".config.txt"
    if os.path.exists(config_file) == False:
        configuration = {"v_card" : 1, "data_directory": "null", "output_directory": "null", "bkup_data_directory": "null", "bkup_output_directory": "null"}
        if os.name == 'nt':
            with open(config_file, "w") as f:
                f.write(json.dumps(configuration))
                os.system("attrib +h config.txt")
        else:
            with open(".config.txt", "w") as f:
                f.write(json.dumps(configuration))
        input(f"        {bcolors.WARNING}Config file not found!{bcolors.END} Press enter to begin initialization.")
        option1()
        return
    else:
        return 

def end_program():
    clear_prompt()
    print(f"""{bcolors.ORANGE}                                                                                                                      
                                        .////.                        
                                   ,////////////                      
                         .//.     /////////////         ...            
                     ./////////  /////////////     /////////          
                  ///////////// /////////////   /////////////         
                ///////////////  //////////// ////////////////        
                ///////////////   ////////// ///////////////          
                //////////////      ///.     /////////////            
                 ///////////       ///////   ////////////             
                    /     /  ////////////////  ///////    .////       
                   /////////////////////////,      //////////////     
                 ///////////////////////////    /////////////////     
                 ////////////////////////////  /////////////////      
                 /////////////////////////////  //////////////        
                  ////////////////////////////  ,///////////          
                    ///////////////////////////  ,///////             
                      //////////////////////////   .                  
                          /////////////////////                       
                               //////// ////.{bcolors.END}\n
                             MICAH THOMAS 2022\n""")   
    exit()



# ===================================================================
#                         INITIALIZER
# ===================================================================

def option1():
    clear_prompt() 
    print(initializer_banner)                                          
    initializer()

    os.chdir(sys.path[0])
    with open(config_file) as f:
        data = f.read()
    configuration = json.loads(data)
    if configuration["output_directory"] == "null" or configuration["data_directory"] == "null":
        print(f"{bcolors.WARNING}One or both directories not declared!{bcolors.END}")
        print("Errors may occur if not properly initialized.")
        input("Press enter to return to the main menu.")
    else:
        input(f"\n{bcolors.GREEN}Initialization Complete.{bcolors.END} Press enter to return to the main menu:")
    return
    







# ===================================================================
#                          UPDATE CODEBOOK
# ===================================================================

def option2():
    clear_prompt()
    print(update_codebook_banner)
    print(f"""
    {bcolors.WARNING}WARNING:{bcolors.END} It is advised that this process be conducted only when new 
    raw data is added. This process: generates individual IDs for the 
    people and income individual pyramids; creates a csv containing all 
    household/individual IDs; and creates variable lists for variable 
    selection. This process can be time intensive as it will iterate 
    through all raw data files.
    \n""")
    advance_strategy = inquirer.confirm("Do you wish to update the codebook?", default=True)
    while advance_strategy is True:
        clear_prompt()
        print(update_codebook_banner)
        print("Initializing Individual ID Generation...")
        id_generator()
        print("Initializing Identifiers Capture...")
        identifiers_capture()
        print("Initializing Variables Capture...")
        variables_capture()
        input(f"\n{bcolors.GREEN}Codebook successfully updated!{bcolors.GREEN} Press enter to continue:")
        break






# ===================================================================
#                       VARIABLE SELECTOR
# ===================================================================

def option3():
    clear_prompt()
    print(variable_selector_banner)
    print(f"""\n
    {bcolors.WARNING}WARNING:{bcolors.END} 
  {bcolors.WARNING}\u25B7{bcolors.END} Selecting large numbers of quarterly variables from the People and 
    Aspirational Pyramids may result in very large sampled panels.
    This could lead to memory constraints and failure to compile. 
  {bcolors.WARNING}\u25B7{bcolors.END} \033[1mHousehold ID, Individual ID, Month, and Month Slot{bcolors.END} 
    are selected by default and are required for merging pyramids.
  {bcolors.WARNING}\u25B7{bcolors.END} This operation overwrites any current variable selector in the directory.
  {bcolors.WARNING}\u25B7{bcolors.END} Merging full pyramids alone can results in output which exceeds 25GB.
    \n""")
    advance_strategy = inquirer.confirm("Do you wish to select new variables? ", default=True)
    while advance_strategy is True:
        clear_prompt()
        print(variable_selector_banner)

        temp_vars = Path(str(config.configure()[0]) + "/codebook/vars_temp.xlsx")
        final_vars = Path(str(config.configure()[0]) +"/codebook/vars_selected.xlsx")

        xls = pd.ExcelFile(Path(str(config.configure()[0]) + "/codebook/vars_all.xlsx"))
        vars_aspirational_quarterly = tuple(list(chain(*((pd.read_excel(xls, 'aspirational_quarterly',header=None)).to_numpy()).tolist())))
        vars_people_quarterly = tuple(list(chain(*((pd.read_excel(xls, 'people_quarterly',header=None)).to_numpy()).tolist())))
        vars_consumption_quarterly = tuple(list(chain(*((pd.read_excel(xls, 'consumption_quarterly',header=None)).to_numpy()).tolist())))
        vars_consumption_monthly = tuple(list(chain(*((pd.read_excel(xls, 'consumption_monthly',header=None)).to_numpy()).tolist())))
        vars_income_monthly_household = tuple(list(chain(*((pd.read_excel(xls, 'income_monthly_household',header=None)).to_numpy()).tolist())))
        vars_income_monthly_individual = tuple(list(chain(*((pd.read_excel(xls, 'income_monthly_individual',header=None)).to_numpy()).tolist())))

        index = 0
        number_of_selected_vars = []
        pyramids = ["Aspirational Quarterly Pyramid", "People Quarterly Pyramid", "Household Consumption Monthly Pyramid", "Household Consumption Quarterly Pyramid", "Individual Income Monthly Pyramid", "Household Income Monthly Pyramid"]
        pyramid_sheet = ["aspirational_quarterly", "people_quarterly", "consumption_monthly", "consumption_quarterly", "income_monthly_individual", "income_monthly_household"]
        with pd.ExcelWriter(temp_vars) as writer:
            for vars in [vars_aspirational_quarterly,vars_people_quarterly,vars_consumption_monthly,vars_consumption_quarterly,vars_income_monthly_individual,vars_income_monthly_household]:
                print(f"{bcolors.WARNING}Current Pyramid: " + str(pyramids[index]) +"\n")
                select_all = inquirer.confirm("Select all variables in this pyramid? ", default=False)
                if select_all is True:
                    print(f"   {bcolors.WARNING}All variables selected. Press enter to continue: {bcolors.END}\n")
                    questions = [
                        inquirer.Checkbox(
                            "interests",
                            message="",
                            choices=vars,
                            default=vars,
                        ),
                    ]
                else:
                    print(f"\n {bcolors.RED}DO NOT DESELECT - (HH_ID, INDIV_ID, MONTH, MONTH_SLOT) - THESE ARE REQUIRED{bcolors.END}\n")
                    questions = [
                        inquirer.Checkbox(
                            "interests",
                            message="Press space to add or remove variables. Press enter to confirm",
                            choices=vars,
                            default=["HH_ID","INDIV_ID","MONTH","MONTH_SLOT"],
                        ),
                    ]
                selected_vars = inquirer.prompt(questions, theme=GreenPassion())
                number_of_selected_vars.append(len(list(selected_vars.values())[0]))
                df = pd.DataFrame(list(selected_vars.values())[0])
                df.to_excel(writer, sheet_name=pyramid_sheet[index], header=False, index=False)
                print("...")
                time.sleep(0.1)
                clear_prompt()
                print(variable_selector_banner)
                index = index+1
        print(
            f"\n{'Variables Selected:':<15}\n",
            f"\n{pyramids[0]:<40}{number_of_selected_vars[0]:>10}",
            f"\n{pyramids[1]:<40}{number_of_selected_vars[1]:>10}",
            f"\n{pyramids[2]:<40}{number_of_selected_vars[2]:>10}",
            f"\n{pyramids[3]:<40}{number_of_selected_vars[3]:>10}",
            f"\n{pyramids[4]:<40}{number_of_selected_vars[4]:>10}",
            f"\n{pyramids[5]:<40}{number_of_selected_vars[5]:>10}","\n\n\n")

        advance_strategy = inquirer.confirm("Do you wish to overwrite existing selected vars? ", default=True)
        if advance_strategy is False:
            os.remove(temp_vars)
            print(f"{bcolors.WARNING}Selected variables not saved.{bcolors.END}")
            input('Press enter to return to the Main Menu: ')
            print(variable_selector_banner)
        else:
            shutil.move(temp_vars, final_vars)
            print(f"{bcolors.GREEN}Selected variables saved.{bcolors.END}")
            input('Press enter to return to the Main Menu: ')
            print(variable_selector_banner)
        break






# ===================================================================
#                           Pyramid Builder
# =================================================================== 

def option4():
    clear_prompt()
    print(pyramid_builder_banner)
    print(f"""\n
    {bcolors.WARNING}WARNING:{bcolors.END} Variables of interest should be selected by using the 
    Variable Selector or by following the instructions in the help menu. 
    Failure to do so can result in panels too large for practical use.
    \n""")  
    advance_strategy = inquirer.confirm("Do you wish to continue construction?", default=True)
    while advance_strategy is True:
        checker = 0
        while checker != 1:
            clear_prompt()
            print(pyramid_builder_banner)
            checker = pyramid_builder()
            if checker == 2:
                pass
            elif checker == 1:
                pass
            else:
                exit_strategy = inquirer.confirm("Re-enter parameters?", default=True)
                if exit_strategy is False:
                    checker = 1
            if checker != 1:
                clear_prompt()
                print(pyramid_builder_banner)
        break






# ===================================================================
#                           HELP
# ===================================================================

def option5():
    clear_prompt()                                           
    #print(help_banner)
    print(f"""{bcolors.GREEN}
    Welcome to the Consumer Pyramids Manager.{bcolors.END} This program is designed 
    to faciliate sampling, building, and managing the CMIE Consumer
    Pyramids Data. There are four menus:\n
      1. \033[1;4mInitializer\033[0m: Allows for setting of the data and output
        directories. In general: the data directory should point to 
        the root of the shared consumerpyramids_india data directory; 
        the output directory should point to the dataready folder 
        contained in the consumerpyramids_india data directory. 
      2. \033[1;4mCodebook Updater\033[0m: Updates the variable list for selection, 
        captures IDs for sampling, and creates unique individual IDs from
        HH_ID and MEM_ID. Typically only run when new pyramids are added
        to the shared data directory.
      3. \033[1;4mVariable Selector\033[0m: Allows for selection on available variables.
      4. \033[1;4mPyramid Builder\033[0m: Allows for construction and sampling of the
        available consumer pyramids.\n
    {bcolors.WARNING}NOTE:{bcolors.END} List of all variables saved to ./codebook/vars_all.xlsx 
    List of selected variables saved to ./codevook/vars_selected.xlsx

    """)
    input('Press enter to return to the Main Menu: ')




# ===================================================================
#                               MAIN
# ===================================================================

def foreman():
    while(True):
        clear_prompt()
        print(welcome_banner)
        config_missing = init()
        clear_prompt()
        print(welcome_banner)
        terminal_menu = TerminalMenu(
            menu_entries=["Initializer", "Update Codebook", "Variable Selector", "Pyramid Builder", "Help", "Exit"],
            menu_cursor="   \u25B6 ",
            menu_cursor_style=("fg_gray", "bold"),
            menu_highlight_style=("standout", "fg_gray"),
            cycle_cursor=True
            )
        menu_entry_index = terminal_menu.show()
        option = menu_entry_index+1

        if option == 1:
            option1()
        elif option == 2:
            option2()
        elif option == 3:
            option3()
        elif option == 4:
            option4()
        elif option == 5:
            option5()
        elif option == 6:
            end_program()
        else:
            print('Invalid option. Please enter a number between 1 and 4.')


    
if __name__ == "__main__":
    foreman()