# Set class

from pyspark.sql.types import StructType, StructField, StringType, DataType, DoubleType
from pyspark.sql.functions import lit, weekofyear, to_date, monotonically_increasing_id, row_number, year, concat_ws
from pyspark.sql.window import Window

class Set:
    
    def month(df, indexnbr_start_month):
        monthlist = []
        date_list = []

        # Extract date strings from DataFrame columns
        for i in range(indexnbr_start_month, len(df.columns)):
            date_list.append((df.columns)[i])

        # Determine distinct months from the date strings
        for d in range(len(date_list)):
            if d > 1 and (d == len(date_list) - 1 or (date_list[d - 1])[0:2] != (date_list[d])[0:2]):
                monthlist.append((date_list[d - 1])[0:2] + (date_list[d - 1])[-2:])

        return monthlist
    
    def week(df, indexnbr_start_week, spark):
        # Select the last three columns of the DataFrame
        df.select(df.columns[-3:]).show()

        # Define the schema for the "slope" column
        schema = StructType([StructField("date", StringType(), True)])

        # Create a DataFrame with the specified schema
        df_date = spark.createDataFrame([(t,) for t in df.columns[indexnbr_start_week:]], schema)
        
        # Convert date strings to date type
        df_date = df_date.withColumn('date', to_date(df_date['date'], 'MM/dd/yy'))

        # Extract week, year, and create a new column "week_year"
        df_date = df_date.withColumn('week', weekofyear(df_date['date']))
        df_date = df_date.withColumn('year', year(df_date['date']))
        week = df_date.withColumn('week_year', concat_ws('/52 A: ', df_date['week'], df_date['year']))
        
        # Collect unique week_year values
        week_list = week.select("week_year").rdd.flatMap(lambda x: x).collect()
        week_list_unique = []

        # Remove duplicates in week_list
        [week_list_unique.append(week) for week in week_list if week not in week_list_unique]

        return week_list_unique
    
    def class_100(df, coeff_slope, spark):
        # Add a unique identifier column to each row
        df = df.withColumn("RowNum", monotonically_increasing_id())
        
        # Define the schema for the "slope" column
        schema = StructType([StructField("slope", DoubleType(), True)])

        # Create an RDD of tuples from coeff_slope
        coeff_slope_rdd = [(float(value),) for value in coeff_slope]

        # Create a DataFrame with the specified schema
        df_coeff = spark.createDataFrame(coeff_slope_rdd, schema)
        
        # Add a row number column ordered by the "slope" column
        windowSpec = Window.orderBy("slope")
        df_coeff = df_coeff.withColumn("RowNum", row_number().over(windowSpec) - 1)
        
        # Join the original DataFrame with the coefficients DataFrame
        df_class = df.join(df_coeff, on="RowNum", how='inner')
        
        # Drop the unique identifier column
        df_class = df_class.drop("RowNum")
        
        # Order the DataFrame by the "slope" column in descending order
        df_class = df_class.orderBy("slope", ascending=False)
        
        # Limit the DataFrame to the top 100 rows
        number_of_line = 100
        df_100 = df_class.limit(number_of_line)
        
        # Drop the "slope" column from the resulting DataFrame
        df_100 = df_100.drop('slope')
        
        # Further limit the DataFrame to the top 50 rows
        df_50 = df_100.limit(50)
        
        return df_100, df_50
