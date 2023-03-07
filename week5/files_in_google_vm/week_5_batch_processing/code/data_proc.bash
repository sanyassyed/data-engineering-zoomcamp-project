# execute this from the terminal to submit a spark job to DataProc
gcloud dataproc jobs submit pyspark \
    --cluster=de-zoomcamp-cluster \
    --region=us-central1 \
    gs://dtc_data_lake_blissful-flames-375219/code/10_spark_locally.py \
    -- \
        --input_green=gs://dtc_data_lake_blissful-flames-375219/pq/green/2020/* \
        --input_yellow=gs://dtc_data_lake_blissful-flames-375219/pq/yellow/2020/* \
        --output=gs://dtc_data_lake_blissful-flames-375219/report-2020










