from flask import Flask, jsonify, render_template
import adafruit_dht
import board
import time

sensor = adafruit_dht.DHT11(board.D4, use_pulseio=False)

app = Flask(__name__)

def read_dht():
    try:
        temperature = sensor.temperature
        humidity = sensor.humidity
        print("Temperature in *C: {:.1f}C, Humidity: {:.1f}%".format(temperature, humidity))
        if humidity is not None and temperature is not None:
            return temperature, humidity
        else:
            return None, None
    except RuntimeError as error:
        print(error)
        time.sleep(2)
        return None, None

@app.route('/')
def index():
    temperature, humidity = read_dht()
    return render_template('main.html', temperature=temperature, humidity=humidity)

@app.route('/data')
def data():
    temperature, humidity = read_dht()
    print("Temperature in *C: {:.1f}*C, Humidity: {:.1f}%".format(temperature, humidity))
    return jsonify(temperature=temperature, humidity=humidity)

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=8080)
    finally:
        sensor.exit()
