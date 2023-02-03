from prefect.deployments import Deployment
from prefect.filesystems import GitHub

github_block = GitHub.load("sanyagithub")
github_flow = github_block.get_directory('homework/week_2_workflow_orchestration/')
github_dep = Deployment.build_from_flow(flow=github_flow.etl_parent_flow, name='Github WebToGcs ETL', work_queue_name="default", storage=github_block)

if __name__=="__main__":
    github_dep.apply()

#`prefect deployment build homework/week_2_workflow_orchestration/etl_web_to_gcs.py:etl_parent_flow -n "Github WebToGcs ETL" -sb github/sanyagithub  -q default --apply`

# REsource
# https://towardsdatascience.com/create-robust-data-pipelines-with-prefect-docker-and-github-12b231ca6ed2