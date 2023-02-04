from prefect.deployments import Deployment
from el_gcs_to_bq import el_parent_flow
from prefect.orion.schemas.schedules import CronSchedule


# Deployment for Q3 Step 2 Loading data to GCS from the web
#local_dep = Deployment.build_from_flow(flow = el_parent_flow, name='GcsToBQ ETL via Python', work_queue_name="default", entrypoint="el_gcs_to_bq.py:el_parent_flow", parameters={"color":"yellow", "months":[2, 3], "year":2019})

# Deployment for Q5 Step 2 Loading data to GCS from the web
local_dep = Deployment.build_from_flow(flow = el_parent_flow, name='GcsToBQ ETL via Python Q5', work_queue_name="default", entrypoint="el_gcs_to_bq.py:el_parent_flow", parameters={"color":"green", "months":[4], "year":2019})

if __name__=="__main__":
    local_dep.apply()


# python .\el_gcs_to_bq_deploy.py
# Build and Apply - use this if you want add parameters after build to the .yaml file
# `prefect deployment build el_gcs_to_bq.py:el_parent_flow -n "GcsToBQ ETL"`
# `prefect deployment apply el_parent_flow-deployment.yaml`