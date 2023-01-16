# docker files begin with FROM keyword to indicate the base IMAGE to start from
FROM python:3.9.1
# will install wget 
RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY ingest_data.py ingest_data.py 

ENTRYPOINT [ "python", "ingest_data.py" ]