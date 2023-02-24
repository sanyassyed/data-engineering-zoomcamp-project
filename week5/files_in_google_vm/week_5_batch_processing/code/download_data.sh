#run from parent of data folder
#Change this files permissions by using : chmod +x download_data.sh
set -e

#TAXI_TYPE=$1 # "yellow"
#YEAR=$2 # 2020

TAXI_TYPES=("yellow" "green")
YEARS=(2020 2021)

#URL_PREFIX="https://s3.amazonaws.com/nyc-tlc/trip+data"
URL_PREFIX="https://github.com/DataTalksClub/nyc-tlc-data/releases/download"


for TAXI_TYPE in "${TAXI_TYPES[@]}"; do
    for YEAR in "${YEARS[@]}"; do
        for MONTH in {1..12}; do
            FMONTH=`printf "%02d" ${MONTH}`
            # because in bash numbers over 7 used in double brackets are treated differently
            if [[ $YEAR == 2021 && ${FMONTH#0} -gt 7 ]]
            then 
                break
            fi
            URL="${URL_PREFIX}/${TAXI_TYPE}/${TAXI_TYPE}_tripdata_${YEAR}-${FMONTH}.csv.gz"

            LOCAL_PREFIX="data/raw/${TAXI_TYPE}/${YEAR}/${FMONTH}"
            LOCAL_FILE="${TAXI_TYPE}_tripdata_${YEAR}_${FMONTH}.csv.gz"
            LOCAL_PATH="${LOCAL_PREFIX}/${LOCAL_FILE}"

            echo "donwloading ${URL} to ${LOCAL_PATH}"
            mkdir -p ${LOCAL_PREFIX}
            wget ${URL} -O ${LOCAL_PATH}

            #echo "compressing ${LOCAL_PATH}"
            #gzip ${LOCAL_PATH}
        done
    done
done