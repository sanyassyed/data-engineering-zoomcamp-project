from prefect.deployments import Deployment
from etl_web_to_gcs import etl_parent_flow
from prefect.orion.schemas.schedules import CronSchedule

# Deployment for Loading data to GCS from the web fhv data for 2019 & 2020
local_dep = Deployment.build_from_flow(flow = etl_parent_flow, name='WebToGcs ETL via Python Wk 3 HW', work_queue_name="week3", entrypoint="etl_web_to_gcs.py:etl_parent_flow", parameters={"months":[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "years":[2020]})


if __name__=="__main__":
    local_dep.apply()

# Go to UI start the agent and run the deployment
# prefect agent start -q "week3"
