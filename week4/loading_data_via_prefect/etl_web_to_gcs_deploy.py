from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import CronSchedule
from etl_web_to_gcs import etl_parent_flow


local_dep = Deployment.build_from_flow(flow = etl_parent_flow, name='WebToGcs ETL Wk 4', work_queue_name="week4", entrypoint="etl_web_to_gcs.py:etl_parent_flow", parameters={"months":[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "years":[2019, 2020], "ftypes":[1], "categories":[1, 2]})

if __name__=="__main__":
    local_dep.apply()

# Go to UI start the agent and run the deployment
# prefect agent start -q "week4"
