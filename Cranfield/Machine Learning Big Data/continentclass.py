from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pycountry_convert as pc
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.window import Window
import matplotlib.pyplot as plt
import folium
import os
from pyspark.sql.functions import monotonically_increasing_id, row_number

class Continent:
    
    @staticmethod
    def get_continent_name(continent_code):
        continent_dict = {
            "NA": "America",
            "SA": "America",
            "AS": "Asia",
            "AF": "Africa",
            "OC": "Oceania",
            "EU": "Europe",
            "AQ": "Antarctica"
        }
        return continent_dict[continent_code]
    
    @staticmethod
    def get_continent(i, lat, long):
        print("get continent of country line " + str(i + 1))
        
        # Use geopy to get location information from latitude and longitude
        geolocator = Nominatim(user_agent="Continent", timeout=10)
        geocode = RateLimiter(geolocator.reverse, min_delay_seconds=1)
        location = geocode(f"{lat}, {long}", language="en")
        
        # For cases where the location is not found, coordinates are Antarctica
        if location is None:
            return "Unknown"
        
        # Extract country code
        address = location.raw["address"]
        country_code = address["country_code"].upper()
        
        # Get continent code from country code
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        continent_name = Continent.get_continent_name(continent_code)
        
        return continent_name

    @staticmethod
    def continent(df, spark):
        df.repartition(5)
        df = df.withColumn("RowNum", monotonically_increasing_id())
        
        df_lat = df.select("Lat").rdd.flatMap(lambda x: x).collect()
        df_long = df.select("Long").rdd.flatMap(lambda x: x).collect()
        
        continent = []
        
        for i in range(df.count()):
            lat = df_lat[i]
            long = df_long[i]
            
            try:
                continent.append(Continent.get_continent(i, lat, long))
            except Exception as e:
                continue
        
        # Define the schema for the "Continent" column
        schema = StructType([StructField("Continent", StringType(), True)])
        
        # Create the DataFrame with the specified schema
        df_continent = spark.createDataFrame([(c,) for c in continent], schema)
        
        windowSpec = Window.orderBy("Continent")
        df_continent = df_continent.withColumn("RowNum", row_number().over(windowSpec) - 1)
        
        df_continent = df_continent.coalesce(1)
        
        df = df.join(df_continent, on="RowNum", how="inner")
        df = df.drop("RowNum")
        df = df.select(*([df.columns[-1]] + [name for name in df.columns[:-1]]))
        
        return df

    @staticmethod
    def cluster_map(df, indexnbr_start_month, monthlist):
        cluster_list = [0, 1, 2, 3]
        index_month = 0
        
        for c in range(indexnbr_start_month, len(df.columns)):
            try:
                print("Map for month: " + str(((df.columns)[c])[8:]))
                
                # Create a folium map
                cluster_map = folium.Map(tiles="cartodb positron", position=[45, 0], zoom_start=2)
                
                os.makedirs("Cluster_map/", exist_ok=True)
                
                # Define the output file path for the map
                if str(((df.columns)[c])[9]) == "/":
                    output_save_map = "Machine Learning Big Data/Cluster_map/" + str(((df.columns)[c])[0:9]) + "_" + str(((df.columns)[c])[10:]) + ".html"
                else:
                    output_save_map = "Machine Learning Big Data/Cluster_map/" + str(((df.columns)[c])[0:10]) + "_" + str(((df.columns)[c])[10:]) + ".html"
                
                cluster_map.save(output_save_map)
                
                # Select relevant columns for the current month
                df_c = df.select(*(df.columns[:4] + [(df.columns)[c]]))
                
                df_c.show()
                
                for cluster in cluster_list:
                    if cluster == 0:
                        color = "blue"
                    elif cluster == 1:
                        color = "red"
                    elif cluster == 2:
                        color = "purple"
                    elif cluster == 3:
                        color = "green"
                    
                    # Filter DataFrame for the current cluster
                    df_cluster = df_c.filter(df_c[(df.columns)[c]] == str(cluster))
                    
                    for i, row in enumerate(df_cluster.collect()):
                        print("Cluster : " + str(cluster) + "  Line : " + str(i))
                        
                        lat = row["Lat"]
                        long = row["Long"]
                        state = row["Province/State"]
                        country = row["Country/Region"]
                        
                        if state is not None:
                            folium.CircleMarker(location=[lat, long], popup=[country, state, cluster], radius=25, fill=True, color=color, fill_color=color).add_to(cluster_map)
                        else:
                            folium.CircleMarker(location=[lat, long], popup=[country, cluster], radius=25, fill=True, color=color, fill_color=color).add_to(cluster_map)
                    
                cluster_map.save(output_save_map)
                
            except Exception:
                print("Error: Memory issue on the RAM")
                break
            
            index_month += 1
        
        return True

    @staticmethod
    def plot_covid_cases(df, countries, index_start_month, name_column, x_name, y_name, title):
        # Select columns for the x-axis (months)
        months_columns = (df.columns)[index_start_month:]

        # Prepare the plot for each country
        for i, country in enumerate(countries):
            # Select data for the specified country
            country_data = df.filter(df[name_column] == country).select(*months_columns).collect()[0]
            
            # Retrieve values for months and COVID cases
            months = months_columns
            cases = [country_data[month] for month in months]
            
            # Define colors for different countries
            colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
            current_color = colors[i % len(colors)]

            # Plot the curve
            plt.plot(months, cases, label=country, color=current_color)

        # Add labels and display the plot
        plt.xlabel(x_name)
        plt.ylabel(y_name)
        plt.title(title)
        plt.legend()
        plt.savefig("Machine Learning Big Data/" + str(title) + ".png")
        # Clear the figure
        plt.clf()

        
    