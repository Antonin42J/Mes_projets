# Find the air quality 

class AirQuality:
    
    # Method to calculate air quality based on PM10 and PM2.5 values
    def airquality(pm10, pm25):
        
        # Convert input values to float
        pm10 = float(pm10)
        pm25 = float(pm25)
        
        # Initialize variables for air quality indices, overall air quality, and air quality range
        pm10air = None
        pm25air = None
        airq = None
        range_air = None
        
        # Define dictionaries for mapping PM values to air quality indices
        dict_airquality_pm1 = {
            (0, 11): 1,
            (12, 23): 2,
            (24, 35): 3,
            (36, 41): 4,
            (42, 47): 5,
            (48, 53): 6,
            (54, 58): 7,
            (59, 64): 8,
            (65, 70): 9,
            (70, float('inf')): 10
        }
        
        dict_airquality_pm2 = {
            (0, 16): 1,
            (17, 33): 2,
            (34, 50): 3,
            (51, 58): 4,
            (59, 66): 5,
            (67, 75): 6,
            (76, 83): 7,
            (84, 91): 8,
            (92, 100): 9,
            (100, float('inf')): 10
        }
        
        dict_range = {
            (0, 3): "Low",
            (4, 6): "Medium",
            (7, 9): "High",
            (10, 11): "Very High"
        }
        
        # Check if both PM10 and PM2.5 values are greater than 0
        if pm10 > 0 and pm25 > 0:
            # Map PM10 value to air quality index
            for key, value in dict_airquality_pm1.items():
                if key[0] <= pm10 <= key[1]:
                    pm10air = value
                    break
                else:
                    pm10air = None
            
            # Adjust PM10 value if not found in the initial mapping
            if pm10air is None:
                pm10 += 1
                for key, value in dict_airquality_pm1.items():
                    if key[0] <= pm10 <= key[1]:
                        pm10air = value
                        break
            
            # Map PM2.5 value to air quality index
            for key, value in dict_airquality_pm2.items():
                if key[0] <= pm25 <= key[1]:
                    pm25air = value
                    break
                else:
                    pm25air = None
            
            # Adjust PM2.5 value if not found in the initial mapping
            if pm25air is None:
                pm25 += 1
                for key, value in dict_airquality_pm2.items():
                    if key[0] <= pm25 <= key[1]:
                        pm25air = value
                        break
            
            # Determine the overall air quality based on PM10 and PM2.5 indices
            if pm10air != pm25air:
                airq = max(pm10air, pm25air)
            else:
                airq = pm10air
            
            # Map the overall air quality index to a range
            for key, value in dict_range.items():
                if key[0] <= airq <= key[1]:
                    range_air = value
                    break
        
        # Return the calculated air quality index and range
        return airq, range_air

        
        