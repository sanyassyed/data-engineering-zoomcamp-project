## Question 1. Load January 2020 data
How many rows does that dataset have?
* Answer : 447,770
* Screenshot of the run:
![OutputQ1](images/logs.jpg) 

## Question 2. Scheduling with Cron
What’s the cron schedule?
* Answer: `0 5 1 * *`
    * Option 1: CLI. Use this command to build, schedule and apply the deployment `prefect deployment build etl_web_to_gcs.py:etl_parent_flow -n "WebToGCS ETL" --cron "0 5 1 * *" --timezone "UTC" -a`
    * Option 2: After bulding and applyting the deployment, set the scheduling via the Orion UI as follows
    ![OutputQ2](images/cron.jpg) 