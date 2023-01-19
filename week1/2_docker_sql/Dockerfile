FROM python:3.9.1
RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY ingest_data.py ingest_data.py

ENTRYPOINT ["python", "ingest_data.py"]

# Commands to execute on bash to first build an image named pandas with the tag test, using the Dockerfile and then run the image to start the container
# docker build -t pandas:test .
# docker run -it pandas:test 2023-01-5 