import paho.mqtt.client as mqtt
from time import time, sleep
import uuid
import requests
import sys
import os

INTERVAL = 1
QOS = 1

topic1="pub_"
topic2="sub_"
sensor_id = "sensor"

path = ""
sub_path = path + "sub_"
pub_path = path + "pub_"
lat_path = path + "latency_"


def on_message(client, userdata, message):
    global sensor_id
    msg = message.payload.decode('utf-8')
    #print(msg)
    f2 = sub_path + sensor_id
    fd2 = open(f2,"a+")
    fd2.write(msg+"\n")
    fd2.close()
    t = msg.split("!")
    print("msg: ",t[0])
    #t2 = time()
    #print("current: ",t2)
    rtt = time() - float(t[0])
    f3 = lat_path + sensor_id
    f = open(f3,"a+")
    f.write(str(rtt)+"\n")
    f.close()

def main(argv):
    global topic1
    global topic2
    global sensor_id
    sensor_id=argv[1]
    host=argv[2]
    port=1883
    #rtt_array = []
    topic1 = topic1+sensor_id
    topic2 = topic2+sensor_id
    data_path = argv[3]

    commands = [
		"rm -f {0}/{1}".format(lat_path,sensor_id),
		"rm -f {0}/{1}".format(pub_path,sensor_id),
		"rm -f {0}/{1}".format(sub_path,sensor_id)
	]
    for cmd in commands:
        os.system(cmd)



    client = mqtt.Client()
    #client2 = mqtt.Client()
    #client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host,port)
    #client.loop_start()
    client.subscribe(topic2, qos=QOS)
    #client2.loop_forever()
    f1 = pub_path + sensor_id
    fd1 = open(f1, "a+")

    for i in range(180):
        r=requests.get(data_path)
        #data = str(time()) + "!" +r.text

        client.loop_start()
        data = str(time()) + "!" +r.text
        client.publish(topic1, data ,qos=QOS)
        client.loop_stop()
        #print(topic2)
        #sleep(INTERVAL)
        #f1 = pub_path + sensor_id
        #fd1 = open(f1,"a+")
        fd1.write(data+"\n")
        #fd1.close()
        #client.subscribe(topic2, qos=QOS)
        #client.loop_stop()
        #t2 = time()
        #print(t2-t1)
        #sleep(INTERVAL)
    #sleep(10)
    #client.loop_stop()
    fd1.close()
    client.loop_forever()

if __name__=="__main__":
    main(sys.argv)
