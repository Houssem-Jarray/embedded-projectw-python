import adafruit_dht
import board
import time
import os

# Sensor data pin is connected to GPIO 4
sensor = adafruit_dht.DHT11(board.D4)

# Variable to control the loop
running = True

# Check if the file exists before opening in 'a' mode
file_exists = os.path.isfile('sensor_readings.txt')
with open('sensor_readings.txt', 'a') as file:
    # Write the header if the file does not exist
    if not file_exists:
        file.write('Time and Date, Temperature ( C), Temperature ( F), Humidity (%)\n')

    # Loop to continuously read sensor data
    while running:
        try:
            # Read temperature and humidity from sensor
            temperature_c = sensor.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = sensor.humidity

            # Print readings on the console
            print(f"Temp={temperature_c:0.1f} C, Temp={temperature_f:0.1f} F, Humidity={humidity:0.1f}%")

            # Save time, date, temperature, and humidity to the file
            file.write(f"{time.strftime('%H:%M:%S %d/%m/%Y')}, {temperature_c:.2f}, {temperature_f:.2f}, {humidity:.2f}\n")

            # Log readings every 10 seconds
            time.sleep(2)
        
        except RuntimeError as error:
            # Handle reading errors gracefully
            print(f"Runtime error: {error.args[0]}")
            time.sleep(2)
            continue
        
        except KeyboardInterrupt:
            # Handle program termination
            print('Program stopped by user.')
            running = False
        
        except Exception as e:
            # Handle any other unexpected errors
            print(f"An unexpected error occurred: {str(e)}")
            running = False
        
    # Clean up the sensor on exit
    sensor.exit()
