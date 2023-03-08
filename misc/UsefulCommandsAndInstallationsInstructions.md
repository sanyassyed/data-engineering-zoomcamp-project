## Docker

### Install vim in docker:

* `apt-get update`
* `apt-get install vim`

### Images running:
* `docker ps`
* `docker pause /(unpause)` -> hibernate
* `docker kill` -> soft shut-down abrupt
* `docker stop / (start,restart)` -> graceful hard shut-down (by unplugging the system)
* `docker down / (up,create)` -> factory reset
[REF:](https://stackoverflow.com/questions/63740108/what-is-the-difference-between-docker-compose-commands-down-kill-and-sto)

* `docker stop container_id`  -> if you want to 
* `docker start container_id` -> to start a container
[REF:](https://app.slack.com/client/T01ATQK62F8/C01FABYF2RG/thread/C01FABYF2RG-1673626584.350539)

### Checking docker networks, containers that are on
* `docker container ls`
* `docker network ls`
* `docker network inspect`
* `container ps`

### docker compose
* `docker-compose up` -> to start docker compose in non-detach mode
* `docker-compose up -d` -> to start docker  compose in detached mode i.e without losing the terminal
* `docker-compose stop` -> to close the containers - use this if you don't want to delete the containers
* `docker-compose down` ->  to shut down the container/s
* `docker-compose down --volumes --rmi all` or  `docker-compose down --volumes --remove-orphans` -> To stop and delete containers, delete volumes with database data, and download images
* `sudo docker info` -> to view docker information


## BASH / WINGW64
### Activating virtual env on WINGW64 
[Look here for details](https://medium.com/@presh_onyee/activating-virtualenv-on-windows-using-git-bash-python-3-7-1-6b4b21640368)
* `cd .my_env`
* `cd Scripts`
* `. activate`
* `deactivate` -> just type that in any directory to deativate the virtual environment

### Other commands
* `cd -` (dash) -> to toggle between two directories
* `cd ../..` -> to go up two directories
* `cd ../../.my_eve/Scripts` -> to go up and into sub directories
* `mkdir name_of_the_directory` -> to create a new directory/folder
* `vim hello.py` -> Create a python file [ref:](https://www.jcchouinard.com/create-python-script-from-terminal/) 



### Setting Environment variables
* Create the environment variables in a file with .bashrc extention eg: `set_env.bashrc`
* Set the environment variables using the keyword 'export' followed by = symbol with no space and its value enclosed in double quotes eg: `export USER='root'`
* Leave the next line empty by pressing enter
* Run the file in bash as follows: `source set_env.bashrc`
* To access the environment variables use `$` sign followed by variable name eg: `echo $USER`
[More Details Here](https://drstearns.github.io/tutorials/env/)
* `printenv` -> The command prints all or the specified environment variables.
* `set` – The command sets or unsets shell variables. When used without an argument it will print a list of all variables including environment and shell variables, and shell functions.
* `echo $SHELL` -> to find which shell it is bash or sh

## POSTGRES
* `TRUNCATE yellow_taxi_data` To delete rows in a table

## PYTHON
* `pip install jupyter` -> to install jupyter notebook
* `jupyter notebook` -> to open/start jupyter notebooks
* `Ctrl + C` -> to close the terminal late

## JUPYTER NOTEBOOK
* `CTRL+Enter` -> Run a cell
* `dd` -> delete a cell (Make sure you have selected the cell first which will change the cell color to blue/gray, green color indicates that cell contents are selected instead)
* `jupyter notebook stop` -> to stop the jupyter notebook

## Useful resources
* [Introduction to command line](https://missing.csail.mit.edu/)
* [How to create terraform files from an existing cloud infrastructure.](https://arivictor.medium.com/turn-your-gcp-project-into-terraform-with-terraformer-cli-eeec36cbe0d8)
* [Evaluation Criteria for the course](https://github.com/alexeygrigorev/mlbookcamp-code/blob/master/course-zoomcamp/cohorts/2022/projects.md#midterm-project)

## Example Capstone Projects by previous cohorts
* [Earthquake Data Engineering capstone project by Nelson A](https://github.com/ANelson82/de_zoomcamp_2022_earthquake_capstone)

## Ubuntu
* `htop` -> to check system configurations
* `ssh -i path_to_private_key username_used_when_created_the_key@external_ip_of_vm` eg: `ssh -i ~/.ssh/gcp sanya@35.205.22.55`
* `ssh de-zoomcamp` -> to ssh into the GCP VM after updating the .ssh config file
* `logout` -> to logout
* `Ctrl+D` -> to logout
* `less .bashrc` -> to view the system config file
* `source .bashrc` -> to logout and and login / will reevaluate the installations and update the VM so you don't have to logout and login after installing something new on the VM 
* `gcloud --version` -> to check the gcloud SDK version on the VM
* `wget url_to_download` -> to download a file/package from a url 
* `wget url_to_download -O <output_file_name>` -> to download a file/package from a url ans saved with a new filename
* `wget url_to_download -P <output_directory>` -> to download a file/package from a url
* `bash path_to_.sh_file` -> to install the package downloaded
* `mv file1_to_move /destination_folder_path` -> move file from one folder to another
* `mkdir path_to_parent_dir/new_dir_name` -> to make a new directory


## Google VM
* `ssh de-zoomcoamp` -> to ssh in to the VM on GCP
* `gcloud auth login` -> to authenticate the VM to login into the project optionally try if you get error `gcloud auth application-default login` Then copy pase the code
* `gcloud config set compute/zone <ZONE>` -> eg: us-central1-c
* `gcloud config unset compute/zone` -> to unset the zone
* ` gcloud compute instances list --project blissful-flames-375219` -> to list the instances in a project on GCP
* `gcloud compute instances start de-zoomcamp --zone us-central1-c --project blissful-flames-375219` ->  to start an instance on GCP
* ``
* `gsutil mv gs://dtc_data_lake_blissful-flames-375219/data/green/ gs://dtc_data_lake_blissful-flames-375219/data_parquet` -> to move files in GCS
* `echo $PATH` -> To view the path varibles
* `sudo shutdown now` -> to shutdown the GCP VM instance from the terminal
* `nano <file_name>` -> to edit a file
* `CTRL + O` -> to save
* `Ctrl + X` -> to exit
* `less yellow_tripdata_2021_01.csv` -> View few rows of the dataset
* `head -n 10 yellow_tripdata_2021-01.csv` -> View first 100 rows of the dataset 
* `head -n 10 yellow_tripdata_2021-01.csv  > yelllow_head.csv` -> Copy first 100 rows of the dataset to a new file
* `wc -l yellow_tripdata_2021-01.csv`-> Count number of rows in the dataset
* `gzip -d -c .\tes.csv.gz | wc -l` -> Count the rows in the gzip file
* `ls |wc -l` -> count number of files in a folder
* `ls -lh` -> list the files in folders with size details, in human readable format
* `ls -lhR name_of_the_folder_with_subfolders` -> lists the contents of the folder and subfolders by going inside. R is for recursively.
* `ls -lr` -> long list format with reverse order while sorting
* `ls -lg` -> like -l but do not list owner
* `la -a` -> this lists all files including the . files
* `tree name_of_the_folder` -> View the folder contents in a tree format
* `screen` -> to start using the screen functionality in a VM
* `CTRL+A+C` -> Clear a screen and have other things running in background. More info [to install screen on VM](https://support.shells.net/hc/en-us/articles/1500003236241-How-to-Open-Multiple-Virtual-Terminal-Windows-on-Ubuntu-20-04-with-Screen) and [using it](https://help.ubuntu.com/community/Screen)
* `CTRL(Hold)+A` -> to go to previous screen
* `screen -r` -> You can re-attach a detached session by typing that
* `date` -> to print system date
* **NOTE:** When starting VM do the following steps
    - Type `screen` and start the screen program that lets you have multiple terminals for 1 VM
    
### Copy file from local to VM server using SFTP (SSH File Transfer Protocol)
* Step 1: Go to the folder on the local machine which has the file to be transfered
* Step 2: Type `sftp ssh_hostname` this will connect you to the root folder in the VM server
* Step 3: Navigate to the destination folder on the VM server
* Step 4: Type `put name_of_the_file_to_transfer` 
* To transfer from remote to local:
    - `get name_of_the_file_to_transfer` -> to transfer a file
    - `get -r name_of_the_folder_to_transfer` -> to transfer a folder


## Git
* `git clone {https link}` -> Anonymously clone a git repo
* `git log --all --oneline` -> List all the commits
* `git show` -> to view the commit message for a specific commit.


## Conda
* [How to activate base in conda](https://carpentries-incubator.github.io/introduction-to-conda-for-data-scientists/02-working-with-environments/index.html#:~:text=Conda%20has%20a%20default%20environment,into%20your%20base%20software%20environment.)
* `conda env list` -> List the conda environments
* `$ conda remove --name my-first-conda-env --all` -> delete an entire environment
* `conda remove --prefix /path/to/conda-env/ --all` -> If you wish to delete and environment that you created with a --prefix option, then you will need to provide the prefix again when removing the environment.

### Creating Virtual env in conda in the project directory
* ` conda create --prefix ./.my_env_conda python=3.10.9 pip` -> Path to install the virtual env in the current project directory with pytho 3.10 and pip
*  `conda activate .my_env_conda` - to activate the virtual env
* `conda activate` -> don't use deactivate just use `activate` to go to base

## Ports
* `netstat -ano | findStr "4200"`
* `tasklist //FI "PID eq 3364"`
* `TaskKill //PID 3364 //F`

## Prefect
* `CTRL + C` -> to stop orion
* `prefect block register -m prefect_gcp` -> to register a block from the prefect_gcp module
* Configure the blocks by going to the blocks tab in the UI and selecting the corresponding block
* `prefect orion start` -> open the open source UI to visually view the flows
* `prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"` -> to configure Prefect to communicate with the server
* `prefect deployment build .\parametarized_flow.py:etl_parent_flow -n "Parameterized ETL"` -> build a deployment via cli `-n` means name of the flow
* `prefect deployment build .\parametarized_flow.py:etl_parent_flow -n "etl2 --cron "0 0 * * *" -a` -> build a deployment via cli `-n` means name of the flow and `--cron` to set the cron job pattern and `-a` to apply that
* `prefect deployment apply .\etl_parent_flow-deployment.yaml ` -> to apply the deployment
* `prefect agent start --work-queue "default"` -> To execute flow runs from this deployment, start an agent that pulls work from the 'default' work queue
* `prefect deployment build --help` -> to view how to set schedule via CLI on a deployment during build
* `prefect deployment --help` -> to view how to set schedule for a given deployment
* `prefect deployment inspect <flow_name>/<deployment_name>` -> You can inspect a deployment using the CLI with the  command, referencing the deployment. This will show the yaml file
* `prefect deployment ls` -> to view the list of deployments
* `prefect deployment run <FLOW_NAME>/<DEPLOYMENT_NAME>` -> to run the deployment from CLI. You can also pass parameters here. Use --help for more info

## dbt
* `dbt run`
* `dbt run --select stg_green_tripdata`
* `dbt run -m stg_green_tripdata`


## Spark
* `spark-shell` - to start spark in linux CLI
* `which java` -> to check if java is installed and where
* `which pyspark` -> to check if pyspark is installed and where
