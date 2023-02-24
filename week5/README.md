# Week 5: Batch Processing Notes

## Introduction
* What is Apache Spark
    - It is a Data Processing Engine
    - It is a multi-language engine and hence can use Java, Scala, Python (using a wrapper PySpark), R etc
    - Spark was written in Scala, that would be the native way of communicating with Spark

## Installation
* [Installing Spark on Linux](https://www.youtube.com/watch?v=hqUbB9c8sKg&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=43)
    1. Install JAVA
        1. Install Java from [open jdk version 11.0.1](https://jdk.java.net/archive/)
        2. Download the file in a new folder called `spark` using
        `wget <link_to_download>`
        3. Unzip the file using the command
        `tar xvzf <name_of_the_file_downloaded>`
        4. Check if you jave the `jdk-11.0.1` folder unzipped
        5. Delete the downloaded file using
        `rm <name_of_the_file_downloaded>`
        6. Set the path to the jdk using the following two commands to create set the variable `JAVA_HOME`
            * `export JAVA_HOME="${HOME}/spark/jdk-11.0.1"`
            * `export PATH="${JAVA_HOME}/bin:${PATH}"`
        7. Perform the path checks using the following commands
        `which java`
        `java --version`
    
    2. Install Spark

* Goto the localhost forwarded port 4040 to view the spark jobs being executed by spark master

## Useful Codes
* To run pyspark in the VM
    ```bash
    export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
    export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"
    ```

## Why use Spark over DataWarehouse SQL? 
* In Spark you can write your own functions and hence it is more flexible. 
* Also many inbuilt functions are available.
* We can do tests and make sure your code works and then execute it on your dataframe
* Things that are not easy to execute in SQL can be easily done spark

## PySpark Important functions 

* `SparkSession` package imported from `pyspark.sql`
* `spark` is an object of type `pyspark.sql.session.SparkSession` (PySpark Dataframe)   
   
    -   ```python
        # to create a PySpark Dataframe object from a csv
        spark_df = spark.read\
             .option("header", "true")\
             .schema(schema)\
             .csv('fhvhv_tripdata_2021-01.csv')
        ``` 

    -  ```python
        # to create a PySpark Dataframe object from a pandas DF where Spark by default infers the schema based on the pandas data types TO PySpark data types.
        spark_df = spark.createDataFrame(pandas_df)
        ``` 
        

* Funtions to use on PySpark DF object
    - ```python
      # To view top rows of Pyspark DF in a table format
      spark_df.show()
      # To view top rows of Pyspark DF as a list
      spark_df.head()
      # To print the schema of the Pyspark DF (similar to .dtypes in pandas)
      spark_df.schema
      # To print schema in a nice tree format
      sparkDF.printSchema()
      ```  