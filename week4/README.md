# Week 4: Analytics Engineering Notes
* `dbt` -> data build tool (Helps with the transformation of data)
*  `Defining a  Deployment Workflow`-> Develop -> Test and Document -> Deployment (Version control and CI/CD)
* dbt Core & dbt Cloud
* Two paths:
    * Big Query which has the dbt core and can connect to dbt Cloud
    * Postgres which will have the dbt core but it cannot connect to dbt cloud so instead you use local IDE and run the dbt models via CLI
* Start dbt project

* Note: DBT Cloud setting: Settings
dbt Cloud will always connect to your warehouse from `52.45.144.63`, `54.81.134.249`, or `52.22.161.231`. Make sure to allow inbound traffic from these IPs in your firewall, and include it in any database grants. 