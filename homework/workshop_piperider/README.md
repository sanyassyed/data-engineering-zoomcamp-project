* [dbt-bigquery connection info](https://www.shipyardapp.com/blog/dbt-core-bigquery/)
* Clone the [week 4 repo](https://github.com/sanyassyed/ny_taxi_rides_zoomcamp) in the VM
    ```bash
    # Create a new branch
    git switch -c develop_piperider
    # Create a profiles.yml file in the current project folder with the following content [Refer this video](https://youtu.be/1HmL63e-vRs?list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&t=159)
        bg-de-zoomcamp:
            target: dev
            outputs:
                dev:
                type: bigquery
                method: service-account
                project: blissful-flames-375219
                dataset: dbt_sanya_models
                threads: 4
                priority: interactive
                keyfile: /home/sanyashireen/.google/credentials/google_credentials.json                
    # Create virtual env with pip installed
    conda create -p ./venv pip
    conda activate venv/
    # install dbt-core and dbt with bigquery adapter and piperider with bigquery adapter
    pip install dbt-core dbt-bigquery 'piperider[bigquery]' python=3.9
    # piprider needs gcloud since its not availble in the virtual env we install it here too
    conda install -c conda-forge google-cloud-sdk

    # Set GCP project details
    gcloud config set project blissful-flames-375219
    
    # Install dbt deps and build dbt models
    dbt deps # downloads the dependencies for current dbt version
    ##################################################################
    # dont update the utils as it gives an error
    # update version to 1.0.0 in the packages.yml file and execute dbt deps again
    dbt deps
    ################################################################
    # test dbt-core and big-query connection
    dbt debug
    # build the models
	dbt build # optional just for 1 model  `dbt build --select stg_yellow_tripdata`
    dbt build --var 'is_test_run: false'
    
    # Initialize PipeRider
    piperider init

    # For Bigquery piperider needs more details
    # More details for piperider BQ adapter here https://docs.piperider.io/reference/supported-data-sources/bigquery-connector

    # Connect to piperider cloud
    piperider cloud signup # enter email and api key
    
    # or
    
    # enter these details to detect login details to pipercloud automatically
    # add it to system root folder ~/.piperider/profile.yml :
    user_id: 12344
	api_token: abc123
    cloud_config:
        default_project: Ssyed/default
        auto_upload: true
    
    
    # Check PipeRider settings
    piperider diagnose
    
    # Run piperider
    piperider run --upload
    ```
* in the models/core/facts_trips.sql add this condition to make sure the year is only 2019 and 2020
```sql
where extract(year from trips_unioned.pickup_datetime) = 2019
or
extract(year from trips_unioned.pickup_datetime) = 2020
```
* And then execute the following
```bash
dbt build --var 'is_test_run: false'
piperider run
# to compare reports
piperider compare-reports --last
```

* Then open the report on Piperider Cloud and the answers for the homework can be found in the report itself under tables/fact_trips tab.