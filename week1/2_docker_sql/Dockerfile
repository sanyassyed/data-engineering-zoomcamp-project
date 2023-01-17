FROM python:3.9

RUN pip install pandas
WORKDIR /app
COPY pipeline.py pipeline.py

ENTRYPOINT ["bash"]

# Commands to execute on bash to first build an image named pandas with the tag test, using the Dockerfile and then run the image to start the container
# docker build -t pandas:test .
# docker run -it pandas:test 2023-01-5 