# Consumer Pyramids Manager
This package is designed to allow for sampling, building, and managing the CMIE Consumer Pyramids Data. The program runs in a command line interface with options for updating the codebook when new data is added, selecting variables of interest, and building/sampling data as needed.
<br/><br/><br/>

## Author:
- Micah Thomas
- [@micah7-clemson] (https://github.com/micah7-clemson)
- (micahdthomas@gmail.com)
<br/><br/><br/>

## MacOS Installation Instructions:
- Install Python 3 (built on 3.10.6)
- Install pip3:
    ```bash
    sudo apt install python3-pip 
    ```
- Install Consumer Pyramids Manager using pip3
    ```bash
    pip3 install package_template
    ```
- Navigate to the directory containing consumer_pyramids_manager-x.x.x.targ.gz. 
- Enter the command below to install the package:
    ```bash
    pip3 install consumer_pyramids_manager-x.x.x.targ.gz
    ```
- The program is now initialized by entering the  ```consumer_pyramids_manager``` command in terminal.
- **NOTE:** Initialization must be run upon first installation.
<br/><br/><br/>

## Windows Installation Instructions:
- Install Python 3 (built on 3.10.6)
- Install pip3: <br />Download the latest version of get-pip.py from
    ```bash
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    ```
    CD into the directory where get-pip.py was downloaded to, and
    enter the following command to install pip3 and its dependencies:
    ```bash
    python3 get-pip.py
    ```
    You can verify that pip3 is installed by navigating to the default 
    pip3 installation directory, eg. C:\python38\scripts\, and enter:
    ```bash
    pip3 --version
    ```
- Add pip3 to system variables:
    - Open the Control Panel and navigate to System.
    - Click on Advanced system settings in the upper left panel.
    - Click on Environment Variables.
    - Under System Variables, scroll down then double-click the PATH variable.
    - Click New, and add the directory where pip3 is installed, e.g. C:\Python38\Scripts , and select OK. 
    <br/>

- Navigate to the directory containing consumer_pyramids_manager-x.x.x.targ.gz. 
- Enter the command below to install the package:
    ```bash
    pip3 install consumer_pyramids_manager-x.x.x.tar.gz
    ```
- The program is now initialized by entering the  ```consumer_pyramids_manager``` command in terminal.
- **NOTE:** Initialization must be run upon first installation.
<br/><br/>

## Running the script without package installation:
- Install Python and pip according to instructions above.
- From the root of the repo enter the following command to install required dependencies:
    ```bash
    pip3 install -r consumer_pyramids_manager/requirements.txt
    ```

- From the root of the repo enter the command:
    ```bash
    python3 consumer_pyramids_manager/foreman.py
    ```
<br/><br/>

## Getting Started:
- **Initialization:** Enables the declaration of data and output directories. Enter the initialization menu to point to the desired locations. The default data directory is the root folder containing the folder: dataraw, codebook, dataready. Where dataraw contains the raw consumer pyramids files from CPME. The default output directory points to the dataready folder in the data directory.<br/><br/>
- **Codebook Updater:** If new data has been added to the dataraw directory or the directory is just established, run codebook updater to pull identifiers, generate individual ids, and prep for variable selection.<br/><br/>
- **Variable Selection:** Allows the researcher to select the desired variables from the available pyramids. It is advised to select on variables after running codebook upater as the default may be to utilize all variables. If you wish to merging a single pyramid, select all variables from only the desired pyramid and keep only the default variables on the others.<br/><br/>
- **Pyramid Builder:** Allows the researcher to sample and construct pyramids using the selected variables.<br/><br/>
- **Help:** Contains basic information for the use of the program.