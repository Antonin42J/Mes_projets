from pyspark.sql.functions import col, monotonically_increasing_id, lit, udf, unix_timestamp, stddev_pop
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans
from pyspark.sql.types import StructType, StructField, StringType
from datetime import datetime
from Setclass import Set
from continentclass import Continent

@udf(StringType())
class Calculation:

    def Average(df_init, df_question, monthlist, indexnbr_start_month):
        # Initialize variables
        index_month = 0
        nbrcprevious = indexnbr_start_month

        # Repartition the initial DataFrame for optimization
        df_init = df_init.repartition(5)

        # Iterate through the columns of the DataFrame
        for c in range(indexnbr_start_month, len(df_init.columns)):
            # Check if it's the last column or a new month has started
            if c == len(df_init.columns) - 1 or (((df_init.columns)[c])[0:2] != monthlist[index_month][0:2]):

                print("Average for month " + str(monthlist[index_month][0:2]) + str(monthlist[index_month][-2:]))
                print()

                # Calculate the mean for the current month
                month_mean = [sum(col(column) for column in df_init.columns[nbrcprevious:c + 1]) / (c - nbrcprevious)]

                # Use the select method to create a new DataFrame with the mean value
                dfq1new = df_init.select(*(["RowNum"] + month_mean))
                dfq1new = dfq1new.withColumnRenamed(dfq1new.columns[1], monthlist[index_month])

                # Join the new DataFrame with the existing one on "RowNum"
                df_question = df_question.join(dfq1new, "RowNum", "inner")

                nbrcprevious = c

                # Move to the next month in the list
                if index_month < len(monthlist) - 1:
                    index_month += 1

        # Drop the temporary "RowNum" column and optimize the DataFrame's partitioning
        df_question = df_question.drop("RowNum")
        df_question = df_question.coalesce(1)

        return df_question

    
    
    def trendline_coeff(df, indexnbr_start_month, spark):
        
        
        coeff_slope = []

        data = df.select(df.columns[indexnbr_start_month:])

        # Display a message indicating the start of the regression computation
        print("Starting regression computation...")

        length_df = data.count()

        # Iterate through each row to perform linear regression
        for i in range(length_df):
            slope = Calculation.Regression_i(i, data, spark)
            coeff_slope.append(slope)

        # Display a message indicating the end of the regression computation
        print("...End of regression computation")

        return coeff_slope
    
    

    def Regression_i(i, data, spark):
            
        # Display a message indicating the start of linear regression for a specific row
        print("Linear regression on line " + str(i + 1) + "/" + str(data.count()))

        x = data.columns
        y = list(data.collect()[i])

        # Create a Spark DataFrame for the specific row
        data_row = zip(x, y)
        df_row = spark.createDataFrame(data_row, ["x", "y"])

        # Transform the date column to Unix timestamp
        df_row = df_row.withColumn("x", unix_timestamp(df_row["x"], "MM/dd/yy"))

        # Use VectorAssembler to transform the DataFrame
        assembler = VectorAssembler(inputCols=["x"], outputCol="features")
        df_row = assembler.transform(df_row)

        # Split the data into training and testing sets
        train_data, test_data = df_row.randomSplit([0.8, 0.2])

        # Perform linear regression
        lr = LinearRegression(featuresCol="features", labelCol="y", regParam=0.01)
        model = lr.fit(train_data)

        # Retrieve the slope coefficient from the model
        slope = model.coefficients[0]

        return slope
    
    
    def standard_deviation(df_mean):
        # Create a new DataFrame to store standard deviations
        df_s_devia = df_mean
        
        # Repartition the DataFrame into 10 partitions
        df_s_devia = df_s_devia.repartition(10)

        # Calculate and print the standard deviation for each column
        for c in range(len(df_mean.columns)):
            print('Standard deviation on week: ' + str((df_s_devia.columns)[c]))
            
            # Calculate standard deviation and replace the original column with the result
            df_s_devia = df_mean.withColumn((df_mean.columns)[c], lit(df_mean.agg(stddev_pop((df_mean.columns)[c])).collect()[0][0]))

        # Reduce the number of partitions to 1
        df_s_devia.coalesce(1)
        
        return df_s_devia


    def average_min_max_df(df_init, df_question, week_list, indexnbr_start_week):
        index_week = 0
        nbrcprevious = indexnbr_start_week
        
        # Initialize DataFrames for average, minimum, and maximum
        df_average = df_question
        df_min = df_question
        df_max = df_question
        
        # Iterate over columns starting from the specified index
        for c in range(indexnbr_start_week, len(df_init.columns)):
            # Determine the week number based on the length of the week string
            week_nbr = 1 if len(week_list[index_week]) == 12 else 2
            
            # Check if the current column corresponds to the current week
            if (c == len(df_init.columns) - 1) or (datetime.strptime((df_init.columns)[c], '%m/%d/%y')).isocalendar()[1] != int((week_list[index_week])[:week_nbr]):
                print("Average min max for week: " + str((week_list[index_week])[:week_nbr]))
                
                # Initialize lists to store sum, min, and max values for each row
                row_sum = []
                row_min = []
                row_max = []
                
                # Repartition the DataFrame into 5 partitions
                df_init = df_init.repartition(5)
                
                # Iterate over rows
                for r in range(df_init.count()):
                    row_list = list((df_init.collect()[r]).asDict().values())
                    row_sum.append(sum(row_list[nbrcprevious:c + 1]))
                    row_min.append(min(row_list[nbrcprevious:c + 1]))
                    row_max.append(min(row_list[nbrcprevious:c + 1]))
                
                # Reduce the number of partitions to 1
                df_init = df_init.coalesce(1)
                
                # Calculate total sum, minimum, and maximum
                somme_totale = sum(row_sum)
                minimum = min(row_min)
                maximum = max(row_max)
                
                try:
                    mean = float(somme_totale / (c - nbrcprevious))
                except Exception:
                    mean = float(mean)
                
                # Handle cases where mean is None
                if mean is None:
                    mean = 0
                
                # Replace columns in the respective DataFrames with calculated values
                df_average = df_average.withColumn(str(week_list[index_week]), lit(mean))
                df_min = df_min.withColumn(str(week_list[index_week]), lit(minimum))
                df_max = df_max.withColumn(str(week_list[index_week]), lit(maximum))
                
                # Update the previous index and move to the next week
                nbrcprevious = c
                if index_week < len(week_list) - 1:
                    index_week += 1
        
        return df_average, df_min, df_max

                
                
    def process_continent(continent, df, week_list, indexnbr_start_week, spark):
        # Filter DataFrame by the specified continent
        df_continent = df.filter(df["Continent"] == continent)

        # Check if the filtered DataFrame is not empty
        if not df_continent.isEmpty():
            # Create a schema for the result DataFrame
            schema = StructType([StructField("Continent", StringType(), True)])
            dfq2 = spark.createDataFrame([(continent,)], schema)

            # Perform calculations for average, standard deviation, min, and max
            df_average_continent, df_min_continent, df_max_continent = Calculation.average_min_max_df(df_continent, dfq2, week_list, indexnbr_start_week)
            df_standard_dev_continent = Calculation.standard_deviation(df_average_continent)

            return df_average_continent, df_standard_dev_continent, df_min_continent, df_max_continent


    def question_2(df, spark):
        # Select relevant columns from the DataFrame
        df = df.select(*([df.columns[0]] + df.columns[6:]))
        
        # Define continent names and starting week index
        continent_6 = ["America", "Oceania", "Asia", "Africa", "Europe", "Antarctica"]
        indexnbr_start_week = 1

        # Select columns related to weeks
        df_week = df.select(df.columns[1:])
       
        # Generate a list of weeks
        week_list = Set.week(df_week, indexnbr_start_week, spark)
        
        # Define the schema for the result DataFrames
        title_schema = ['Continent'] + week_list
        schema = StructType([StructField(name, StringType(), True) for name in title_schema])
        
        # Initialize DataFrames for average, standard deviation, min, and max
        df_average = spark.createDataFrame([], schema)
        df_standard_dev = spark.createDataFrame([], schema)
        df_min = spark.createDataFrame([], schema)
        df_max = spark.createDataFrame([], schema)
        
        # Iterate over continents
        for continent in continent_6:
            print("Continent: " + str(continent))
            
            try:
                # Process the continent and retrieve the results
                df_average_continent, df_standard_dev_continent, df_min_continent, df_max_continent = Calculation.process_continent(continent, df, week_list, indexnbr_start_week, spark)
            except Exception:
                # Handle exceptions and create empty DataFrames
                df_average_continent = spark.createDataFrame([], schema)
                df_standard_dev_continent = spark.createDataFrame([], schema)
                df_min_continent = spark.createDataFrame([], schema)
                df_max_continent = spark.createDataFrame([], schema)
            
            # Union the continent results to the overall DataFrames
            if df_average_continent:
                df_average = df_average.union(df_average_continent)
            if df_standard_dev_continent:
                df_standard_dev = df_standard_dev.union(df_standard_dev_continent)
            if df_min_continent:
                df_min = df_min.union(df_min_continent)
            if df_max_continent:
                df_max = df_max.union(df_max_continent)
        
        # Reduce the number of partitions to 1 for each DataFrame
        df_average = df_average.coalesce(1)
        df_standard_dev = df_standard_dev.coalesce(1)
        df_min = df_min.coalesce(1)
        df_max = df_max.coalesce(1)
        
        try:
            # Generate plots for average, max, min, and standard deviation
            list_continent_graph = ["Europe", "Asia", "Africa", "Oceania", "America"]
            Continent.plot_covid_cases(df_average, list_continent_graph, indexnbr_start_week, "Continent", "Week", "Average_covid", "Week_average_covid_continent")
            Continent.plot_covid_cases(df_max, list_continent_graph, indexnbr_start_week, "Continent", "Week", "Max_covid", "Week_max_covid_continent")
            Continent.plot_covid_cases(df_min, list_continent_graph, indexnbr_start_week, "Continent", "Week", "Min_covid", "Week_min_covid_continent")
            Continent.plot_covid_cases(df_standard_dev, list_continent_graph, indexnbr_start_week, "Continent", "Week", "sdevia_covid", "Week_sdevia_covid_continent")
        except Exception:
            print("Plot error")
        
        # Write the DataFrames to CSV files
        df_average.write.mode("overwrite").option("header", True).option("delimiter", ",").csv("MLBD_Assigment/continent_mean.csv")
        df_standard_dev.write.mode("overwrite").option("header", True).option("delimiter", ",").csv("MLBD_Assigment/continent_standard_deviation.csv")
        df_min.write.mode("overwrite").option("header", True).option("delimiter", ",").csv("MLBD_Assigment/continent_min.csv")
        df_max.write.mode("overwrite").option("header", True).option("delimiter", ",").csv("MLBD_Assigment/continent_max.csv")

            
            
    def cluster(df_init, indexnbr_start_month, monthlist):
        index_month = 0
        nbrcprevious = indexnbr_start_month
        
        # Add a unique identifier column to each row
        df_init = df_init.withColumn("RowNum", monotonically_increasing_id())
        
        # Select relevant columns for the clustering process
        df_question = df_init.select(df_init.columns[:4])
        df_question = df_question.withColumn("RowNum", monotonically_increasing_id())

        for c in range(indexnbr_start_month, len(df_init.columns) - 1):
            # Check if the current column corresponds to the current month
            if (c == len(df_init.columns) - 1) or (((df_init.columns)[c])[0:2] != monthlist[index_month][0:2]):
                print("Cluster for month " + str(monthlist[index_month][0:2]) + str(monthlist[index_month][-2:]))

                # Select columns for the current month
                df_month = df_init.select(df_init.columns[nbrcprevious:c + 1])

                # Assemble features for KMeans clustering
                feature_cols = df_month.columns
                assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
                df_month = assembler.transform(df_month)

                # Apply KMeans clustering with k=4
                kmeans = KMeans(featuresCol="features", predictionCol="cluster", k=4, seed=1)
                model = kmeans.fit(df_month)
                df_cluster_month = model.transform(df_month)

                # Select relevant columns for the result DataFrame
                dfq3new1 = df_cluster_month.select("cluster")
                dfq3new1 = dfq3new1.withColumnRenamed("cluster", "cluster_" + str(monthlist[index_month]))

                dfq3new2 = df_init.select("RowNum")
                dfq3new1 = dfq3new1.withColumn("index", monotonically_increasing_id())
                dfq3new2 = dfq3new2.withColumn("index", monotonically_increasing_id())

                # Join the cluster information with the original DataFrame
                dfq3new = dfq3new1.join(dfq3new2, "index", "inner")
                df_question = df_question.join(dfq3new, "RowNum", "inner")

                # Drop unnecessary columns
                df_question = df_question.drop("index")

                # Update the previous index and move to the next month
                nbrcprevious = c
                if index_month < len(monthlist) - 1:
                    index_month += 1

        # Drop the unique identifier column
        df_question = df_question.drop("RowNum")

        # Reduce the number of partitions to 1 for the result DataFrame
        df_question = df_question.coalesce(1)

        return df_question

    
