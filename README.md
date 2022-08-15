# Consumer Pyramids Manager
This package is designed to allow for sampling, building, and managing the CMIE Consumer Pyramids Data. The program runs in a command line interface with options for updating the codebook when new data is added, selecting variables of interest, and building/sampling data as needed.
<br/><br/>

## Author:
- Micah Thomas
- (micahdthomas@gmail.com)
<br/><br/>

## Installation Instructions (MacOS and Windows):
- Install Python 3 (built on 3.10.6)
- Download pip:
    ```bash
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    ```
- Install pip:
    ```bash
    python3 get-pip.py
    ```
- Manually install package dependencies (pip3 throws error if done within .tar.gz). From the root of the repo, enter the following command:
    ```bash
    cat requirements.txt | xargs pip install
    ```
- Install the consumer_pyramids_manager.<br/> From the root of the repo, enter the following command:
    ```bash
    pip3 install dist/*.tar.gz
    ```
- The program can now be called by entering the  ```consumer_pyramids_manager``` command in terminal.

- **NOTE:** Initialization must be run upon first installation.
<br/><br/>

## Windows Installation Instructions Addendum:
- Due to compatibility errors with some of the dependencies, all of the above instructions must be completed within Windows Subsystem for Linux (WSL2). Install according to your machine's instructions then follow the instructions as normal. 
- It is possible that pip will not automatically populate in the system variables, to correct this follow these steps:
    - Open the Control Panel and navigate to System.
    - Click on Advanced system settings in the upper left panel.
    - Click on Environment Variables.
    - Under System Variables, scroll down then double-click the PATH variable.
    - Click New, and add the directory where pip3 is installed, e.g. C:\Python38\Scripts , and select OK. 
    <br/><br/>

## Alternate Installation:
- In the event of dependency clash or failure to install, these instructions enable manual operation. Follow the installation instructions as laid out above, but skip the last step installing the consumer_pyramids_manager package. Instead, once the dependencies are installed, from the root of the src folder, run the following command:
    ```bash
    python3 src/foreman.py
    ```
<br/>


## Program Menus:
- **Initialization:** Enables the declaration of data and output directories. Enter the initialization menu to point to the desired locations. The default data directory is the root folder containing the folder: dataraw, codebook, dataready. Where dataraw contains the raw consumer pyramids files from CPME. The default output directory points to the dataready folder in the data directory.<br/><br/>
- **Codebook Updater:** If new data has been added to the dataraw directory or the directory is just established, run codebook updater to pull identifiers, generate individual ids, and prep for variable selection.<br/><br/>
- **Variable Selection:** Allows the researcher to select the desired variables from the available pyramids. It is advised to select on variables after running codebook upater as the default may be to utilize all variables. If you wish to merging a single pyramid, select all variables from only the desired pyramid and keep only the default variables on the others. **Variables can also be selected outside the program by copying desired variables from ```./codebook/vars_all.xlsx``` to ```./codebook/vars_selected.xlsx``` after generation is completed by the codebook updater.**<br/><br/>
- **Pyramid Builder:** Allows the researcher to sample and construct pyramids using the selected variables.<br/><br/>
- **Help:** Contains basic information for the use of the program.
<br/><br/>

## Data Directory Setup:
The data directory containing the raw data files from CMIE Consumer Pyramids must be structured as follows. Dataready is a default output folder, but can be changed within the program. 

    data_directory 
        ├── codebook  
        ├── dataready  
        └── dataraw  
           ├── aspirational
           │   └── quarterly
           │       ├─- aspirational_india_YYYYMMDD_YYYYMMDD_R.csv
           |       └── ...
           ├── consumption
           │   ├── monthly
           │   │   ├── consumption_pyramids_YYYYMMDD_MS_rev.csv
           │   │   └── ...
           │   └── quarterly
           │       ├── consumption_pyramids_YYYYMMDD_YYYYMMDD_R.csv
           │       └── ...
           ├── income
           │   └── monthly
           │       ├── household
           │       │   ├── household_income_YYYYMMDD_MS_rev.csv
           │       │   └── ...
           │       └── individual
           │           ├── member_income_YYYYMMDD_MS_rev.csv
           │           └── ...
           └── people
               └── quarterly
                   ├── people_of_india_YYYYMMDD_YYYYMMDD_R.csv
                   └── ...

