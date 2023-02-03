# Week 2: Workflow Orchestration - Prefect

## Video 2.2.2 [Introduction to Prefect Concepts](https://www.youtube.com/watch?v=cdtN6dhp708&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=19)
1. Run Docker-Compose to start a Postgres & PgAdmin container on the same network (with the postgres 5432 port exposed for data push and pull from local system inot/out of Postgres)
2. Pull data (.csv.gz file) from the web -> Write to local system
3. Read from local system (using read_csv) and modify column dtypes
4. Clean the dataset in a function -> Load data into the postgres (in a container) using SqlAlchemyConnector Block
5. Check data loaded into Postgres using Pgadmin (in the same container)

## Video 2.2.3 [ETL with GCP & Prefect](https://www.youtube.com/watch?v=W-rMz_2GwqQ&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=20)
1. Pull data (.parquet file) from the web (using read_csv function)
2. Clean/Transform the data -> Store data on local system
3. Read from local system and write to GCS Bucket (using GcsBucket Block) 


## Video 2.2.4 [From Google Cloud Storage to Big Query](https://www.youtube.com/watch?v=Cx5jt-V5sgE&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=21)
1. Pull data (.parquet file) from Google Cloud Storage (using GCS Bucket Block)
2. Store data on local system
3. Read data from local system 
4. Clean/Transform the data
5. Write data to a table in the dataset in a project on Big Query (using GcpCredentials Block)

## Video 2.2.5 [Parametrizing Flow & Deployments with ETL into GCS flow](https://www.youtube.com/watch?v=QrDxPjX10iw&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=22)
### Parameterization: 
* Same as Video 2.2.3 but running sub-flows from the main flow for each month by passing a list [1,2,3] of parameters. So in the end we have yellow taxi data for the three months on the local system and GCS bucket
### Parameterization & Deployment:
* Build & Deployment of this same thing via CLI 
    1. Write the python file with the flows, sub-flows and tasks
    2. Build a Deployment 
    3. Apply the Deployment to parameterize the flow via an agent
    4. Execute the flow via an agent pulling from the default workqueue (Here we are starting the agent and it is now turned on and listenning to perform any tasks that are scheduled)

## Video 2.2.6 [Schedules & Docker Storage with Infrastructure](https://www.youtube.com/watch?v=psNSzqTsi-s&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=23)
* How to schedule deployments either by Interval, Cron or RRule(Recurring rules).
* CRON (* * * * * - Minutes Hour Day_Of_The_Month Month_Number Day_Of_The_Week ) Each star represents the following (Eg: 22 3 4 1 2 means At 03:22 AM on Tuesday or on day 4 of the month, only in January)
* Three options for setting the schedule / scheduling:
    * Option 1: You can set the CRON schedule via command line during build and apply as follows `prefect deployment build etl_web_to_gcs.py:etl_parent_flow -n "WebToGCS ETL" --cron "*/1 * * * *" -a` (Hint: use `prefect deployment build --help` for more info) [Documentation Link](https://docs.prefect.io/concepts/deployments/?h=prefect+deployment)
    * Option 2: After build & apply via command line using `set-schedule` (Hint: use `prefect deployment --help` for more info)
    * Option 3: After build and apply via Orion UI.
* Prefect flows on Docker Container:
* Store our code on Docker Image. Build an image from the Dockerfile using the command `docker image build -t sanyasyed/prefect:zoom .`
* Put it up /Publish the Docker image on Docker Hub using the command `docker image push sanyasyed/prefect:zoom`
* Make a `Docker Container` block using the blocks tab in the Prefect Orion UI
* Run the Docker container and our flow code will be available there and from there we deploy our flow and run it via the container using the same steps as in video 2.2.5 but via a python file and cli (USing a python file to build, and apply the flow and then running it so the agent can catch it)

