import adafruit_dht
import board
from flask import Flask, jsonify, render_template
import time

# Sensor data pin is connected to GPIO 4
sensor = adafruit_dht.DHT11(board.D4, use_pulseio=False)

app = Flask(__name__)

# Function to read data from DHT11 sensor
def read_dht():
    try:
        # Read temperature and humidity from sensor
        temperature_c = sensor.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = sensor.humidity
        print("Temperature in *C: {:.1f}*C, Temperature in *F: {:.1f}*F, Humidity: {:.1f}%".format(temperature_c, temperature_f, humidity))
        if humidity is not None and temperature_c is not None:
            return temperature_c, temperature_f, humidity
        else:
            return None, None, None
    except RuntimeError as error:
        print(error)
        time.sleep(2)  # Add delay to avoid rapid looping on error
        return None, None, None

# Route to serve the static HTML template
@app.route('/')
def index():
    # Read temperature and humidity from sensor
    temperature_c, temperature_f, humidity = read_dht()
    try:
        return render_template('index.html', temperature_c=temperature_c, temperature_f=temperature_f, humidity=humidity)
    except Exception as e:
        print("Error rendering template:", e)
        return "Error rendering template", 500

# Route to serve sensor data in JSON format (for auto-updating via JavaScript)
@app.route('/data')
def data():
    temperature_c, temperature_f, humidity = read_dht()
    print("Temperature in *C: {:.1f}*C, Temperature in *F: {:.1f}*F, Humidity: {:.1f}%".format(temperature_c, temperature_f, humidity))
    return jsonify(temp_c=temperature_c, tempe_f=temperature_f, hum=humidity)

# Main program
if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=8080)
    finally:
        sensor.exit()  # Clean up GPIO state on exit
