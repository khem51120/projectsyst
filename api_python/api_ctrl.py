import cmd
from time import time
from flask import Flask, jsonify, render_template, request
import requests
import pymysql
import json
from flask_cors import CORS

from flask import Flask
from flask_mqtt import Mqtt

app = Flask(__name__)

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000/*"}})

app.config['MQTT_BROKER_URL'] = '150.95.30.172'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'PowerSyst'
app.config['MQTT_PASSWORD'] = '1234'
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
mqtt = Mqtt(app)



@app.route('/onDoor',methods=['post'])
def onDoor():
    j = request.get_json()
    print(j)
    #print('Door ON')
    cmd = j["cmd"]
    m_topic = "power/"
    print(m_topic)
    mqtt.publish(m_topic, cmd)
    return cmd

@app.route('/offDoor',methods=['get'])
def offDoor():
    #j = request.get_json()
    #print(j)
    print('Door OFF')
    return 'Door OFF'

@app.route('/savetime',methods=['post'])
def savetime():
    j = request.get_json()
    print(j)
    timestart = j["starttime"].split(":",1)
    print(timestart[0])
    print(timestart[1])
    h_on = timestart[0]
    m_on = timestart[1]
    timeend = j["endtime"].split(":",1)
    print(timeend[0])
    print(timeend[1])
    h_off = timeend[0]
    m_off = timeend[1]
      
    #database connection
    connection = pymysql.connect(host="localhost",user="root",passwd="",database="power_system" )

    cursor = connection.cursor()
    if j["type"] == 1 :
        day = 0
        if j["day"] == "อาทิตย์" :
            day = 1
        elif j["day"] == "จันทร์" :
            day = 2
        elif j["day"] == "อังคาร" :
            day = 3
        elif j["day"] == "พุธ" :
            day = 4   
        elif j["day"] == "พฤหัสบดี" :
            day = 5
        elif j["day"] == "ศุกร์" :
            day = 6
        elif j["day"] == "เสาร์" :
            day = 7
        print (day)  
        cursor.execute("INSERT INTO time_week(dayname,H_on,M_on,H_off,M_off) VALUES(%s,%s,%s,%s,%s)",(str(day),h_on,m_on,h_off,m_off))
    elif j["type"] == 2 :
        cursor.execute("INSERT INTO time_day(daystart,H_on,M_on,dayend,H_off,M_off) VALUES(%s,%s,%s,%s,%s,%s)",(j["daystart"],h_on,m_on,j["dayend"],h_off,m_off))
    connection.commit()
    connection.close()
    return j

@app.route('/sendapigate',methods=['post'])
def sendapi():
    j = request.get_json()
    print(j)
    
    m_topic = "donausDev/"+ j["camID"] + "/cmd" 
    # # b4e62d6dd4c6
    # m_topic = "donausDev/b4e62d6dd4c6/event"
    print(m_topic)
    mqtt.publish(m_topic, j["cmd"])
    
    if j["cmd"] == 'capture_on' or j["cmd"] == 'capture_off' :
        r = requests.post('https://maker.ifttt.com/trigger/'+ j["event"] + '/json/with/key/' + j["key_ifttt"])
        print(r)

    return jsonify(j)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='4003', use_reloader=True)