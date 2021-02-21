import random
import time
import Adafruit_DHT

from paho.mqtt import client as mqtt_client


broker = 'IPadresse' #IP Boker eingeben
port = 1883 #Port Boker eingeben
topic = "/nistkasten/Temperatur"
topic2 = "/nistkasten/Luftfeuchte"
# generate client ID with pub prefix randomly
client_id = 'Nistkasten'
username = 'user' #username eingeben
password = 'Passwort' #passwort eingeben
sensor = Adafruit_DHT.DHT22
gpio = 27 #GPIO an dem der DHT22 haengt

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(30)
        humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
        msg1 = '{0:0.1f}'.format(temperature,humidity)
        msg2 = '{1:0.1f}'.format(temperature,humidity)
        result = client.publish(topic, msg1)
        result2 = client.publish(topic2, msg2)



def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
