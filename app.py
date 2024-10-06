from flask import Flask, render_template, jsonify
import mysql.connector

app = Flask(__name__)

# Function to establish database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root_123',
        database='swell_wave_v2'
    )
    return connection

# Route to render the index page
@app.route('/')
def index():
    return render_template('index.html')

# Location
latitude = 7.1033120
longitude = 125.7188463

# Route to fetch current swell data
@app.route('/current_swell')
def current_swell():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Query for current swell data filtered by location
    query = '''
    SELECT time, swell_wave_height, swell_wave_direction, swell_wave_period
    FROM current_swell
    WHERE location_id = (
        SELECT location_id FROM locations WHERE latitude = %s AND longitude = %s
    )
    ORDER BY time DESC LIMIT 1;
    '''
    cursor.execute(query, (latitude, longitude))
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(result)

# Route to fetch hourly swell data
@app.route('/hourly_swell')
def hourly_swell():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Query for hourly swell data filtered by location
    query = '''
    SELECT time, swell_wave_height, swell_wave_direction, swell_wave_period
    FROM hourly_swell
    WHERE location_id = (
        SELECT location_id FROM locations WHERE latitude = %s AND longitude = %s
    )
    ORDER BY time;
    '''
    cursor.execute(query, (latitude, longitude))
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(results)

# Route to fetch the location data
@app.route('/location')
def location():
    
    location_data = {
        'latitude': latitude,
        'longitude': longitude
    }

    return jsonify([location_data])


if __name__ == '__main__':
    app.run(debug=True)
