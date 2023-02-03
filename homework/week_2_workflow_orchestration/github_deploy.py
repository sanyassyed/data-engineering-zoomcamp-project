from prefect.deployments import Deployment
from prefect.filesystems import GitHub
from etl_web_to_gcs import etl_parent_flow

github_block = GitHub.load("sanyagithub")
github_dep = Deployment.build_from_flow(flow = etl_parent_flow, name='Github WebToGcs ETL-File', work_queue_name="default", storage=github_block, entrypoint="homework/week_2_workflow_orchestration/etl_web_to_gcs.py:etl_parent_flow")

if __name__=="__main__":
    github_dep.apply()

#`prefect deployment build homework/week_2_workflow_orchestration/etl_web_to_gcs.py:etl_parent_flow --path homework/week_2_workflow_orchestration/ -n "Github WebToGcs ETL" -sb github/sanyagithub  -q default --apply`

# REsource
# https://towardsdatascience.com/create-robust-data-pipelines-with-prefect-docker-and-github-12b231ca6ed2
# , parameters={"color":"green", "months":[9, 10],"year":2020}