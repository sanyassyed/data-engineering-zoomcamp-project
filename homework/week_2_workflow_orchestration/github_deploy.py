from prefect.deployments import Deployment
from prefect.filesystems import GitHub
from etl_web_to_gcs import etl_parent_flow

github_block = GitHub.load("sanyagithub")
github_flow = github_block.get_directory(from_path='homework/week_2_workflow_orchestration', local_path=".")
github_dep = Deployment.build_from_flow(flow=etl_parent_flow, name='Github WebToGcs ETL', work_queue_name="default")

if __name__=="__main__":
    github_dep.apply()

#`prefect deployment build -n "Github WebToGcs ETL" -sb github/sanyagithub --apply 'homework/week_2_workflow_orchestration'/etl_web_to_gcs.py:etl_parent_flow`