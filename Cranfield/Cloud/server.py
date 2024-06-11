import asyncio
import websockets
import mysql.connector
import json

# Definition of the asynchronous server function
async def server(websocket, path):
    
    # Continuously receive messages from clients
    while True:
        # Receive message
        message = await websocket.recv()
        message_list = message.split('//')
        
        try:
            # Extract client and message details
            client = message_list[0][1:]
            message_r = message_list[1][:-1]
            print("message received: ", message_r, " from " + client) 
        except Exception:
            # If extraction fails, use the original message
            message_r = message
            print("message received: ", message_r)
        
        # Process messages, for example, store in RDS database
        if "Download sensors list" in message_r:
            try:
                db = connectiondatabase()
            except Exception:
                print("Database out") 
                await websocket.send("Database out")
                break
                
            await download_sensors_list(db, websocket)
                 
        elif "Download data" in message_r: 
            try:
                data = None
                db = connectiondatabase()
            except Exception: 
                print("Database out")
                await websocket.send("Database out")
                break
            
            await download_data(db, data, websocket)
            
        else:
            # For other messages, treat them as data and process accordingly
            data = message_r
            print(f"Received data: {data}")
            
            data_dict = json.loads(data)
            
            try: 
                db = connectiondatabase()
                        
            except Exception: 
                print("Database out")
                await websocket.send("Database out")
                break
            
            await download_data(db, data_dict, websocket)
            
# Function to establish a database connection
def connectiondatabase():
    db = mysql.connector.connect(host="airqualitydata.cprfleavtufk.us-east-1.rds.amazonaws.com", 
                                 user="admin", database="airquality", password="airq1234", port=3306)
    return db

# Function to format sensor list results into JSON
async def download_sensors_list(db, websocket):
    cursor = db.cursor()
    
    sql = """
        SELECT * FROM sensors_list;    
    """

    cursor.execute(sql)
    result = cursor.fetchall()
    formated_result = format_results_sensors(result)
    
    cursor.close()
    
    await websocket.send(str(formated_result))

# Function to format data results into JSON
async def download_data(db, data, websocket):
    cursor = db.cursor()
        
    if data is None:
        sql = """
            SELECT air_quality_data.id_balise, air_quality_data.timestamp, air_quality_data.pm10, air_quality_data.pm25, air_quality_data.airquality, 
            air_quality_data.qualification, sensors_list.latitude, sensors_list.longitude, sensors_list.altitude, sensors_list.country_code, sensors_list.country_name
            FROM air_quality_data
            JOIN sensors_list ON air_quality_data.id_balise = sensors_list.id_balise;
        """
    else:
        # Build SQL query based on filter criteria
        sql = """
            SELECT air_quality_data.id_balise, air_quality_data.timestamp, air_quality_data.pm10, air_quality_data.pm25, air_quality_data.airquality, 
            air_quality_data.qualification, sensors_list.latitude, sensors_list.longitude, sensors_list.altitude, sensors_list.country_code, sensors_list.country_name
            FROM air_quality_data
            JOIN sensors_list ON air_quality_data.id_balise = sensors_list.id_balise 
            WHERE
        """        

        if data['ids'] != '':
            sql += "air_quality_data.id_balise = '" + str(data['ids']) +"' AND "
            
        if data['lat'] != '':
            sql += "sensors_list.latitude = '" + str(data['lat']) +"' AND "
            
        if data['long'] != '':
            sql += "sensors_list.longitude = '" + str(data['long']) +"' AND "
            
        if data['alt'] != '':
            sql += "sensors_list.altitude = '" + str(data['alt']) +"' AND "
            
        if data['country_code'] != '':
            sql += "sensors_list.country_code = '" + str(data['country_code']) +"' AND "
        
        if data['country_name'] != '':
            sql += "sensors_list.country_name = '" + str(data['country_name']) +"' AND "
            
        if data['starttime'] != '' and data['endtime'] != '':
            sql += "air_quality_data.timestamp BETWEEN '" + str(data['starttime']) + "' AND '" + str(data['endtime']) +"' AND "
            
        if data['starttime'] == '' and data['endtime'] != '':
            sql += "air_quality_data.timestamp BETWEEN (SELECT MIN(timestamp) FROM air_quality_data) AND '" + str(data['endtime']) + "' AND "
            
        if data['starttime'] != '' and data['endtime'] == '':
            sql += "air_quality_data.timestamp BETWEEN '" + str(data['starttime']) + "' AND SELECT MAX(timestamp) FROM air_quality_data) AND "
            
        if sql[-2] =="D":
            sql = sql[:-4]
            sql += ";"
            
        if sql[-1] == "E":
            sql = sql[:-5]
            sql += ";"

    cursor.execute(sql)
    result = cursor.fetchall()
    formated_result = format_results_data(result)
    
    cursor.close()
    
    await websocket.send(str(formated_result))
        
# Function to format data results into JSON
def format_results_data(results):
    formatted_results = []
    for row in results:
        formatted_row = {
            'id_balise': str(row[0]),
            'timestamp': str(row[1].strftime('%Y-%m-%d %H:%M:%S')),
            'pm10': str(row[2]),
            'pm25': str(row[3]),
            'airquality': str(row[4]),
            'qualification': str(row[5]),
            'latitude': str(row[6]),
            'longitude': str(row[7]),
            'altitude': str(row[8]),
            'country_code': str(row[9]),
            'country_name': str(row[10])
        }
        formatted_results.append(formatted_row)
        
    json_data = json.dumps(formatted_results, indent=2)
    return json_data

# Function to format sensor list results into JSON
def format_results_sensors(results):
    formatted_results = []
    for row in results:
        formatted_row = {
            'id_balise': str(row[1]),
            'latitude': str(row[2]),
            'longitude': str(row[3]),
            'altitude': str(row[4]),
            'country_code': str(row[5]),
            'country_name': str(row[6])
        }
        formatted_results.append(formatted_row)
        
    json_data = json.dumps(formatted_results, indent=2)
    return json_data

# Main function to start the server
def main_server():
    start_server = websockets.serve(server, "0.0.0.0", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

# Run the main server function if this script is executed
if __name__ == "__main__":
    main_server()
