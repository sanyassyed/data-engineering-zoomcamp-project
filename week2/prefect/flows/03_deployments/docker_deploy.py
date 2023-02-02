from prefect.deployments import Deployment
from parametarized_flow import etl_parent_flow
from prefect.infrastructure.docker import DockerContainer

docker_block = DockerContainer.load("zoom")

docker_dep = Deployment.build_from_flow(flow=etl_parent_flow, name='docker-flow', infrastructure=docker_block)

if __name__=="__main__":
    docker_dep.apply()

# To build and apply i.e deploy the flow via the container run the following command, we can then view the Deployment `docker-flow` under the Deployment tab in the UI
# `python .\flows\03_deployments\docker_deploy.py``
# View the profiles available on prefect using the command
# `prefect profile ls``
# Set the prefect api url again the Docker Container is able to interface with the orion server
# `prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api`
# Start up the agent to look for work from the default work queue
# `prefect agent start -q default`
# Run the flow from CLI
#`prefect deployment run etl-parent-flow/docker-flow -p "months=[1,2]"`