import requests
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Define the latitude and longitude
latitude = 7.103312
longitude = 125.7188463

# Fetch data from API
url = f'https://barmmdrr.com/connect/gmarine_api?latitude={latitude}&longitude={longitude}&hourly=swell_wave_height,swell_wave_direction,swell_wave_period,swell_wave_peak_period'
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    # Connect to the database
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root_123',
            database='swell_wave_v2'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Create tables if they do not exist
            create_locations_table = '''
            CREATE TABLE IF NOT EXISTS locations (
                location_id INT PRIMARY KEY AUTO_INCREMENT,
                latitude DECIMAL(10, 7) NOT NULL,
                longitude DECIMAL(10, 7) NOT NULL,
                elevation DECIMAL(5, 2),
                location_name VARCHAR(100)
            );
            '''
            create_units_table = '''
            CREATE TABLE IF NOT EXISTS units (
                unit_id INT PRIMARY KEY AUTO_INCREMENT,
                time_unit VARCHAR(50),
                interval_unit VARCHAR(50),
                swell_wave_height_unit VARCHAR(50),
                swell_wave_direction_unit VARCHAR(50),
                swell_wave_period_unit VARCHAR(50)
            );
            '''
            create_current_swell_table = '''
            CREATE TABLE IF NOT EXISTS current_swell (
                current_swell_id INT PRIMARY KEY AUTO_INCREMENT,
                location_id INT NOT NULL,
                time DATETIME NOT NULL,
                swell_wave_height DECIMAL(5, 2) NOT NULL,
                swell_wave_direction DECIMAL(5, 2),
                swell_wave_period DECIMAL(5, 2),
                FOREIGN KEY (location_id) REFERENCES locations(location_id)
            );
            '''
            create_hourly_swell_table = '''
            CREATE TABLE IF NOT EXISTS hourly_swell (
                hourly_swell_id INT PRIMARY KEY AUTO_INCREMENT,
                location_id INT NOT NULL,
                time DATETIME NOT NULL,
                swell_wave_height DECIMAL(5, 2) NOT NULL,
                swell_wave_direction DECIMAL(5, 2),
                swell_wave_period DECIMAL(5, 2),
                FOREIGN KEY (location_id) REFERENCES locations(location_id)
            );
            '''
            cursor.execute(create_locations_table)
            cursor.execute(create_units_table)
            cursor.execute(create_current_swell_table)
            cursor.execute(create_hourly_swell_table)

            # Insert location data or fetch location_id
            select_location_query = '''
            SELECT location_id FROM locations WHERE latitude = %s AND longitude = %s;
            '''
            cursor.execute(select_location_query, (latitude, longitude))
            location_result = cursor.fetchone()

            if location_result:
                location_id = location_result[0]  # Use the existing location ID
            else:
                insert_location_query = '''
                INSERT INTO locations (latitude, longitude) VALUES (%s, %s);
                '''
                cursor.execute(insert_location_query, (latitude, longitude))
                location_id = cursor.lastrowid  # Get the new location ID

            # Insert units data (assuming units are part of the API response)
            units_data = data.get('units', {})
            if units_data:
                insert_units_query = '''
                INSERT INTO units (time_unit, interval_unit, swell_wave_height_unit, swell_wave_direction_unit, swell_wave_period_unit)
                VALUES (%s, %s, %s, %s, %s);
                '''
                cursor.execute(insert_units_query, (
                    units_data.get('time', 'hour'),
                    units_data.get('interval', 'hourly'),
                    units_data.get('swell_wave_height', 'm'),
                    units_data.get('swell_wave_direction', 'degrees'),
                    units_data.get('swell_wave_period', 's')
                ))

            # Insert hourly swell data
            hourly_data = data.get('hourly', {})
            timestamps = hourly_data.get('time', [])
            swell_wave_heights = hourly_data.get('swell_wave_height', [])
            swell_wave_directions = hourly_data.get('swell_wave_direction', [])
            swell_wave_periods = hourly_data.get('swell_wave_period', [])

            # Check if all lists have the same length
            if len(timestamps) == len(swell_wave_heights) == len(swell_wave_directions) == len(swell_wave_periods):
                for i in range(len(timestamps)):
                    timestamp_str = timestamps[i]
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M')  # Adjusted format
                    swell_wave_height = swell_wave_heights[i]
                    swell_wave_direction = swell_wave_directions[i]
                    swell_wave_period = swell_wave_periods[i]

                    # Handle NULL values: set default value or skip insertion
                    if swell_wave_direction is None:
                        swell_wave_direction = 0.0  # Assign default value, can be adjusted based on your needs
                    if swell_wave_period is None:
                        swell_wave_period = 0.0
                    
                    # Insert into hourly_swell
                    insert_hourly_swell_query = '''
                    INSERT INTO hourly_swell (location_id, time, swell_wave_height, swell_wave_direction, swell_wave_period)
                    VALUES (%s, %s, %s, %s, %s)
                    '''
                    cursor.execute(insert_hourly_swell_query, (location_id, timestamp, swell_wave_height, swell_wave_direction, swell_wave_period))

                # Insert current swell data (use latest timestamp or first entry)
                current_time = timestamps[0]  # Assuming first entry is the most recent
                current_swell_height = swell_wave_heights[0]
                current_swell_direction = swell_wave_directions[0]
                current_swell_period = swell_wave_periods[0]

                insert_current_swell_query = '''
                INSERT INTO current_swell (location_id, time, swell_wave_height, swell_wave_direction, swell_wave_period)
                VALUES (%s, %s, %s, %s, %s);
                '''
                cursor.execute(insert_current_swell_query, (
                    location_id, current_time, current_swell_height, current_swell_direction, current_swell_period
                ))

                # Commit the transaction
                connection.commit()
            else:
                print("Error: Data lists have different lengths.")

    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
else:
    print(f"Failed to retrieve data: {response.status_code}")
