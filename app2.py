from flask import Flask, render_template
import paho.mqtt.client as mqtt

app = Flask(__name__)

# MQTT settings
mqtt_broker = "broker.emqx.io"
mqtt_port = 1883
mqtt_topic = "HEALTH"

# Flask route for home page
@app.route('/')
def index():
    return render_template('index2.html', data=device_data)

# MQTT on_connect callback function
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(mqtt_topic)

# Dictionary to store data for each device
device_data = {"device1": None, "device2": None}

# MQTT on_message callback function
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    data = msg.payload.decode('utf-8')
    mac_id = data.split(',')[0]

    if mac_id == "e4:5f:01:f1:22:11":
        device_data["device1"] = data
    elif mac_id == "e4:5f:01:d7:4c:37":
        device_data["device2"] = data

    print("Device data:", device_data)

# Set up MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port, 60)

# Run MQTT client in a background thread
client.loop_start()

if __name__ == '__main__':
    app.run(debug=True)
