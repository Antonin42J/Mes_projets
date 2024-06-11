# Main function for MLBD Assignment

# Library
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, monotonically_increasing_id
from multiprocessing import Pool
from functools import partial

# Class
from Setclass import Set
from Verificationclass import Verification
from continentclass import Continent
from Calculationclass import Calculation
import time

# Start time
start = time.time()

# Construction of Spark session
spark = SparkSession.builder.appName("MLBD") \
    .config("spark.sql.legacy.timeParserPolicy", "LEGACY") \
    .getOrCreate()

# DataFrame
dfc19_file = spark.read.csv("Machine Learning Big Data/time_series_covid19_confirmed_global.csv", header=True, inferSchema=True)
dfc19 = dfc19_file

# Display the first 10 columns of the DataFrame
dfc19.select(dfc19.columns[:10]).show()

# Question 1: DataFrame modification
dfc19_row = dfc19.withColumn("RowNum", monotonically_increasing_id())
dfc19 = dfc19_row.select(*(["RowNum"] + dfc19.columns))

# Initialization of question 1 DataFrame
dfq1 = dfc19.select(dfc19.columns[:5])
dfq1_verif = dfc19.select(dfc19.columns[1:5])

# Question 1: Calculate average COVID cases per month
indexnbr_start_month = 5
dfc19 = dfc19.repartition(10)
monthlist = Set.month(dfc19, indexnbr_start_month)
dfq1 = Calculation.Average(dfc19, dfq1, monthlist, indexnbr_start_month)

# Question 1 Verification
dfq1_verif = Verification.question1_verifcation_pandas()

# Resetting dfc19
dfc19 = dfc19.drop("RowNum")
dfq1 = dfq1.coalesce(1)
dfq1 = dfq1.orderBy("Country/Region")

# Important element for plot
list_country_graph = ["Spain", "South Africa", "Uruguay"]
name_column = "Country/Region"
x_name = "Month"
y_name = "Average_covid"
title = "Month_average_covid"

# Plot COVID cases 
Continent.plot_covid_cases(dfq1, list_country_graph, indexnbr_start_month-1, name_column, x_name, y_name, title)

# Save the plot as an image
dfq1.write.mode("overwrite").option("header", True).option("delimiter", ",").csv("Machine Learning Big Data/average.csv")
dfq1_verif.to_csv('Machine Learning Big Data/average_verif.csv', index=False, header=True)

# Question 2:
dfc19 = dfc19_file
indexnbr_start_day = 5

# Calculate trendline coefficient
coeff_slope = Calculation.trendline_coeff(dfc19, indexnbr_start_day, spark)

# Select 100 (50 for question 3) countries based on trendline coefficient
df_100, df_50 = Set.class_100(dfc19, coeff_slope, spark)
df_100.repartition(10)

# Order by continent
df_100_continent = Continent.continent(df_100, spark)
df_100_continent.repartition(10)

# Answer to question 2
Calculation.question_2(df_100_continent, spark)

# Question 3
indexnbr_start_month = 4
df_50 = df_50.repartition(10)

# Cluster the selected 50 countries based on monthly COVID cases
df_cluster = Calculation.cluster(df_50, indexnbr_start_month, monthlist)
df_cluster = df_cluster.coalesce(1)

# Save the clustered data as a CSV file
df_cluster.write.mode("overwrite").option("header", True).option("delimiter", ",").csv("Machine Learning Big Data/cluster.csv")

# Generate and save cluster maps for selected months
Continent.cluster_map(df_cluster, indexnbr_start_month, monthlist)

# End time
end = time.time()

# Total time spent on the execution
total_time = end - start

# Convert the elapsed time to hours, minutes, and seconds
hours, remainder = divmod(total_time, 3600)
minutes, seconds = divmod(remainder, 60)
time_spend = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

print(time_spend)

# Stop Spark session
spark.stop()





