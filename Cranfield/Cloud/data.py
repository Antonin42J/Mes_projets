import mysql.connector
import os
import boto3
import json
import csv
import pandas as pd
from sqlalchemy import create_engine

from airquality import AirQuality
from country import Country


class DataBase :
    
    def connectiondatabase() :
        # Establishes a connection to the MySQL database
        db = mysql.connector.connect(host="airqualitydata.cprfleavtufk.us-east-1.rds.amazonaws.com", 
                                     user="admin", database="airquality", password="airq1234", port=3306)
        return db
    
    def create_table(db, sql_text) :
        # Creates a table in the database based on the provided SQL query
        cursor = db.cursor()
        sql = sql_text
        cursor.execute(sql)
        cursor.close()
        return 0
    
    def sensors(db, data_file):
        # Manages sensors-related data and updates the sensors_list table in the database
        cursor = db.cursor()
        sql_sensors_list = """
            CREATE TABLE IF NOT EXISTS sensors_list (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_sensors INT,
                latitude FLOAT,
                longitude FLOAT,
                altitude FLOAT,
                country_code VARCHAR(255),
                country_name VARCHAR(255)
            );
        """
        DataBase.create_table(db, sql_sensors_list)
        
        cursor.execute("SELECT * FROM sensors_list;")
        sensor = cursor.fetchall()
        cursor.close()

        with open(data_file, "r") as filejson :
            data_file = json.load(filejson)
            existing_id = []

            for row in sensor :
                if row[0] != "id" :
                    existing_id.append(row[1])

            title = [['id_sensors', 'latitude', 'longitude', 'altitude', 'country_code', 'country_name']]

            with open("sensorfile.csv", "w", newline='') as sensorfile :
                row_w = []
                writer = csv.writer(sensorfile)
                writer.writerows(title)

                for s in data_file :
                    if s["sensordatavalues"][0]["value_type"] == "P1" :
                        id = s["location"]["id"]
                        if id not in existing_id :
                            lat = s["location"]["latitude"]
                            long = s["location"]["longitude"]
                            altitude = s["location"]["altitude"]
                            country_code = s["location"]["country"]
                            country_name = Country.convert_name(country_code)
                            row_w.append([id, lat, long, altitude, country_code, country_name])
                            existing_id.append(id)

                if row_w != [] :
                    writer.writerows(row_w)

            sensorfile.close()

        filejson.close()

        df = pd.read_csv("sensorfile.csv", encoding='ISO-8859-1')

        engine = create_engine('mysql+mysqlconnector://admin:airq1234@airqualitydata.cprfleavtufk.us-east-1.rds.amazonaws.com:3306/airquality')
        df.to_sql("sensors_list", con=engine, if_exists='append', index=False)
        os.remove("sensorfile.csv")
        engine.dispose()
        
    def airquality_func(db, data_file):
        # Manages air quality-related data and updates the air_quality_data table in the database
        cursor = db.cursor()
        sql_sensors_list = """
            CREATE TABLE IF NOT EXISTS air_quality_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_sensors INT,
                timestamp DATETIME,
                pm10 FLOAT,
                pm25 FLOAT,
                airquality INT,
                qualification VARCHAR(255)
            );
        """
        DataBase.create_table(db, sql_sensors_list)
        cursor.execute("SELECT * FROM air_quality_data;")
        airq = cursor.fetchall()
        cursor.close()

        with open(data_file, "r") as filejson :
            data_file = json.load(filejson)
            time_id = []

            for row in airq :
                if row[0] != "id" :
                    time_id.append([row[1], (row[2]).strftime("%Y-%m-%d %H:%M:%S")])

            title = [['id_sensors', 'timestamp', 'pm10', 'pm25', 'airquality', 'qualification']]

            with open("airqfile.csv", "w", newline='') as airqfile :
                row_w = []
                writer = csv.writer(airqfile)
                writer.writerows(title)

                for a in data_file :
                    if a["sensordatavalues"][0]["value_type"] == "P1" :
                        id = a["location"]["id"]
                        timestamp = a["timestamp"]
                        if [id, timestamp] not in time_id :
                            try :
                                pm10 = a["sensordatavalues"][0]["value"]
                            except IndexError :
                                pm10 = 0
                            try :
                                pm25 = a["sensordatavalues"][1]["value"]
                            except IndexError :
                                pm25 = 0
                            air_quality, range_air = AirQuality.airquality(pm10, pm25)
                            row_w.append([id, timestamp, pm10, pm25, air_quality, range_air])
                            time_id.append([id, timestamp])

                if row_w != [] :
                    writer.writerows(row_w)

            airqfile.close()

        filejson.close()

        df = pd.read_csv("airqfile.csv", encoding='ISO-8859-1')
        engine = create_engine('mysql+mysqlconnector://admin:airq1234@airqualitydata.cprfleavtufk.us-east-1.rds.amazonaws.com:3306/airquality')
        df.to_sql("air_quality_data", con=engine, if_exists='append', index=False)
        os.remove("airqfile.csv")
        engine.dispose()
        
    def drop_table(db) :
        # Drops existing tables in the database
        cursor = db.cursor()
        sql = """
            DROP TABLE IF EXISTS air_quality_data, sensors_list;
        """
        cursor.execute(sql)
        cursor.close()
        db.close()
        
    def main_database(file) :
        # Main function to manage the entire database process
        db = DataBase.connectiondatabase()
        s3_client = boto3.client('s3')
        s3_client.download_file("airqualitydatastorage", "airqualityJSONfile/"+file, file)
        DataBase.sensors(db, file)
        DataBase.airquality_func(db, file)
        os.remove(file)
        db.close()

