from prefect.deployments import Deployment
from etl_web_to_gcs import etl_parent_flow
from prefect.orion.schemas.schedules import CronSchedule

# Deployment for Q1
#local_dep = Deployment.build_from_flow(flow = etl_parent_flow, name='WebToGcs ETL via Python', work_queue_name="default", entrypoint="etl_web_to_gcs.py:etl_parent_flow", parameters={"color":"green", "months":[1], "year":2020})

# Deployment for Q2
#local_dep = Deployment.build_from_flow(flow = etl_parent_flow, name='WebToGcs ETL with Scheduling via Python', work_queue_name="default", entrypoint="etl_web_to_gcs.py:etl_parent_flow", parameters={"color":"green", "months":[2], "year":2020}, schedule = (CronSchedule(cron="0 5 1 * *", timezone="UTC")))

# Deployment for Q3 Step 1 Loading data to GCS from the web
#local_dep = Deployment.build_from_flow(flow = etl_parent_flow, name='WebToGcs ETL via Python-Q3', work_queue_name="default", entrypoint="etl_web_to_gcs.py:etl_parent_flow", parameters={"color":"yellow", "months":[2, 3], "year":2019})

# Deployment for Q5 Step 1 Loading data to GCS from the web
local_dep = Deployment.build_from_flow(flow = etl_parent_flow, name='WebToGcs ETL via Python-Q5', work_queue_name="default", entrypoint="etl_web_to_gcs.py:etl_parent_flow", parameters={"color":"green", "months":[4], "year":2019})


if __name__=="__main__":
    local_dep.apply()

# Go to UI start the agent and run the deployment

# Q1
# Optional CLI
# prefect deployment build etl_web_to_gcs.py:etl_parent_flow -n "WebToGCS ETL"
# prefect deployment apply etl_parent_flow-deployment.yaml

# Q2
# Optional CLI
# Build & Schedule & Apply in 1 step
# `prefect deployment build etl_web_to_gcs.py:etl_parent_flow -n "WebToGCS ETL" --cron "0 5 1 * *" --timezone "UTC" -a`



# Documentation
# https://docs.prefect.io/api-ref/prefect/deployments/#prefect.deployments.Deployment.build_from_flow