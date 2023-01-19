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

* `docker stop container_id`  - if you want to 
* `docker start container_id` - to start a container
[REF:](https://app.slack.com/client/T01ATQK62F8/C01FABYF2RG/thread/C01FABYF2RG-1673626584.350539)

### Checking docker networks, containers that are on
* `docker container ls`
* `docker network ls`
* `docker network inspect`
* `container ps`

### docker compose
* `docker-compose up` to start docker compose in non-detach mode
* `docker-compose up -d` to start docker  compose in detached mode i.e without losing the terminal
* `docker-compose down` to close the containers 


## BASH / WINGW64
### Activating virtual env on WINGW64 
[Look here for details](https://medium.com/@presh_onyee/activating-virtualenv-on-windows-using-git-bash-python-3-7-1-6b4b21640368)
* `cd .my_env`
* `cd Scripts`
* `. activate`
* `deactivate` just type that in any directory to deativate the virtual environment

### Other commands
* `cd -` (dash) to toggle between two directories
* `cd ../..` to go up two directories
* `cd ../../.my_eve/Scripts` to go up and into sub directories

### BASH commands for the csv file

* `less yellow_tripdata_2021_01.csv` - View few rows of the dataset
* `head -n 10 yellow_tripdata_2021-01.csv` - View first 100 rows of the dataset 
* `head -n 10 yellow_tripdata_2021-01.csv  > yelllow_head.csv` - Copy first 100 rows of the dataset to a new file
* `wc -l yellow_tripdata_2021-01.csv`- Count number of rows in the dataset


### Setting Environment variables
* Create the environment variables in a file with .bashrc extention eg: `set_env.bashrc`
* Set the environment variables using the keyword 'export' followed by = symbol with no space and its value enclosed in double quotes eg: `export USER='root'`
* Run the file in bash as follows: `source set_env.bashrc`
* To access the environment variables use `$` sign followed by variable name eg: `echo $USER`
[More Details Here](https://drstearns.github.io/tutorials/env/)

## POSTGRES
* `TRUNCATE yellow_taxi_data` To delete rows in a table

## PYTHON
* `pip install jupyter` - to install jupyter notebook
* `jupyter notebook` - to open/start jupyter notebooks
* `Ctrl + C` - to close the terminal late
* `vim hello.py` - Create a python file [ref:](https://www.jcchouinard.com/create-python-script-from-terminal/) 