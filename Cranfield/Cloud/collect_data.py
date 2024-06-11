#Collect data

import json
import logging
import boto3
from botocore.exceptions import ClientError
import os
import requests
import time

from data import DataBase


class CollectData :

    # def upload_file_S3(file_json,bucket,old_timestamp) :
        

    #     response = requests.get(file_json)
    #     s3_client = boto3.client('s3')

    #     file_name = (file_json.split("/")[-1])
    #     key = "airqualityJSONfile/" + file_name
        
    #     timestamp = CollectData.timestamp_verification(response)
        
    #     transfer = False
        
    #     if old_timestamp != timestamp:
            
    #         old_timestamp = timestamp
            
    #         with open(file_name, 'wb') as file:
    #             file.write(response.content)
    #         file.close()
            
    #         data = open(file_name,"rb")

    #         try:
    #             s3_client.put_object(Key = key, Body = data, Bucket = bucket)
                
    #         except ClientError as e:
    #             logging.error(e)
                
    #         data.close()
    #         os.remove(file_name)
            
    #         print("File air quality at : " + str(timestamp))
            
    #         transfer = True
            
        
    #     return old_timestamp, transfer
    
    
    def upload_file_S3(file_json, bucket):
        # Retrieve the content of the JSON file from the specified URL
        response = requests.get(file_json)
        
        # Create an S3 client
        s3_client = boto3.client('s3')

        # Extract the file name from the URL
        file_name = (file_json.split("/")[-1])

        # Define the S3 key for storing the file
        key = "airqualityJSONfile/" + file_name

        # Extract the timestamp from the JSON response using the timestamp_verification function
        timestamp = CollectData.timestamp_verification(response)

        # Save the content of the file locally
        with open(file_name, 'wb') as file:
            file.write(response.content)
        file.close()

        # Open the local file in binary read mode
        data = open(file_name, "rb")

        try:
            # Upload the file to the specified S3 bucket with the given key
            s3_client.put_object(Key=key, Body=data, Bucket=bucket)
        except ClientError as e:
            # Log an error if the upload fails
            logging.error(e)

        # Close the local file
        data.close()

        # Remove the local file after uploading to S3
        os.remove(file_name)

        # Print a message indicating the successful upload along with the timestamp
        print("File air quality at: " + str(timestamp))

    # Function to extract timestamp from the response of a JSON file
    def timestamp_verification(response):
        # Parse the JSON data from the response
        data = json.loads(response.text)
        
        # Extract the timestamp from the first element in the data
        timestamp_data = data[0]
        timestamp = timestamp_data["timestamp"]
        
        return timestamp

    
    
# def main_collect_data() :
    
#     file = "data.json"
    
#     file_json = 'https://data.sensor.community/static/v2/' + file
#     bucket = "airqualitydatastorage"
    
#     old_timestamp = 0
    
#     db = DataBase.connectiondatabase()
    
#     DataBase.drop_table(db)

#     while True :
        
#         try :  
#             old_timestamp, transfer = CollectData.upload_file_S3(file_json,bucket,old_timestamp)
            
#             if transfer == True : 
#                 print("Beginning of tranfer to database")
                
#                 DataBase.main_database(file)
                
#                 print("End of transfer to database \n")
            
#         except Exception as e:
#             print(e)
#             False

def main_collect_data():
    # Specify the JSON file, S3 bucket, and create a database connection
    file = "data.json"
    file_json = 'https://data.sensor.community/static/v2/' + file
    bucket = "airqualitydatastorage"
    db = DataBase.connectiondatabase()
    
    # Drop the existing table in the database
    DataBase.drop_table(db)

    # Continuous loop for collecting and transferring data
    while True:
        # Upload the JSON file to S3
        CollectData.upload_file_S3(file_json, bucket)
        
        # Print a message indicating the beginning of the transfer to the database
        print("Beginning of transfer to database")
        
        # Transfer data from S3 to the database
        DataBase.main_database(file)
        
        # Print a message indicating the end of the transfer to the database
        print("End of transfer to database \n")
        
        # Pause execution for 300 seconds (5 minutes) before the next iteration
        time.sleep(300)

# Entry point to the script, execute the main_collect_data function
if __name__ == "__main__":
    main_collect_data()





