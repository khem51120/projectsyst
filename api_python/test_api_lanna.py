from re import I
from flask import Flask, jsonify, render_template, request
import requests
import pymysql
import json
from datetime import datetime, timedelta

app = Flask(__name__)

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')




@app.route('/datalog')
def datalog():
    token = request.args.get('token')
    id = request.args.get('id')
    v1 = request.args.get('V1')
    v2 = request.args.get('V2')
    v3 = request.args.get('V3')
    a1 = request.args.get('A1')
    a2 = request.args.get('A2')
    a3 = request.args.get('A3')
    p1 = request.args.get('P1')
    p2 = request.args.get('P2')
    p3 = request.args.get('P3')
    e = request.args.get('E')
    # print(j["token_id"])
    # json_val1 = j["device"]
    # json_val2 = j["temp"]
    # json_val3 = j["humid"]
    #database connection
    connection = pymysql.connect(host="localhost",user="root",passwd="rootsql@MoDiFy002",database="test_api_db" )

    cursor = connection.cursor()
    cursor.execute("INSERT INTO power_meter(token, id, v1, v2, v3, a1, a2, a3, p1, p2, p3, e) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(token,id,v1,v2,v3,a1,a2,a3,p1,p2,p3,e))
    #insert = "INSERT INTO Sensor_data(token, temp, humid) VALUES(%s,%s,%s)",(j["token_id"],j["temp"],j["humid"]);"
    # list_db = "Select token from token_db where token = ('" + j["token_id"] + "');"
    # cursor.execute(list_db)
    # rows = cursor.fetchall()
    # for row in rows :
    #     print(row[0])
    #     data = row[0]

    # if data == j["token_id"] :
    #     #executing the quires
    #     if j["type"] == "241" :
    #         cursor.execute("INSERT INTO power_meter(token, no_device, volt, curr, power, unit) VALUES(%s,%s,%s,%s,%s,%s)",(j["token_id"],j["device"],j["volt"],j["curr"],j["power"],j["unit"]))
    #     elif j["type"] == "160" :
    #         cursor.execute("INSERT INTO flow_meter(token, no_device, flow) VALUES(%s,%s,%s)",(j["token_id"],j["device"],j["flow"]))
    #commiting the connection then closing it.
    connection.commit()
    connection.close()

    return '200'


@app.route('/line_notify', methods=['post'])
def line_notify():
    url = 'https://notify-api.line.me/api/notify'
    
    j = request.get_json()
    #tokens = j["tokens"]
    # token = tokens
    #database connection
    connection = pymysql.connect(host="localhost",user="root",passwd="rootsql@MoDiFy002",database="smartfarmDB" )

    cursor = connection.cursor()
    
    # queries for retrievint all rows
    #retrive = "Select token, temp, humid  from Sensor_data WHERE " + j["tokens"] + " = token order by num desc;"
    retrive = "Select token, line_token from line_token where token in ('" + j["token_id"] + "') order by num desc limit 1;"
    #executing the quires
    cursor.execute(retrive)
    rows = cursor.fetchall()
    # data = {}
    # myJson = []
    line_token = ""
    for row in rows :
        print(row)
        line_token = row[1]
        # data = {'token' : row[0], 'line_token': row[1]}
        # myJson.append(data)
        # data = {}
    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+ line_token}
    msg = j["msg"]
    r = requests.post(url, headers=headers , data = {'message':msg})

    #commiting the connection then closing it.
    connection.commit()
    connection.close()
    # json_string = jsonify(myJson)
    # print(json_string)

    return r.text

@app.route('/getdata_last_1h/<tokens>',methods=['get'])
def getdata_last_1h(tokens):
    now = datetime.now() # current date and time
    last = timedelta(hours=-1)
    last_time = now + last 
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    curr_time = last_time.strftime("%Y-%m-%d %H:%M:%S")

    print(date_time)
    print(curr_time)
    print(tokens)
    # j = request.get_json()
    # tokens = j["tokens"]

    # token = tokens
    #database connection
    connection = pymysql.connect(host="localhost",user="root",passwd="rootsql@MoDiFy002",database="smartfarmDB" )

    cursor = connection.cursor()
    list_db = "Select data_base from token_db where token = ('" + tokens + "');"
    cursor.execute(list_db)
    data_row = cursor.fetchall()
    db = ""
    for row in data_row :
        print(row)
        db = row[0]

    data = {}
    myJson = []

    # queries for retrievint all rows
    #retrive = "Select token, temp, humid  from Sensor_data WHERE " + j["tokens"] + " = token order by num desc;"
    if db == "flow_meter" :
        retrive = "Select no_device, flow, time from flow_meter where token = ('" + tokens + "') and time >= ('" + curr_time + "') and time <= ('" + date_time + "');"
        #executing the quires
        cursor.execute(retrive)
        rows = cursor.fetchall()
        for row in rows :
            print(row)
            data = {'id': row[0], 'flow' : row[1], "time" : row[2].strftime("%Y-%m-%d %H:%M:%S")}
            # json_string = jsonify(data)
            myJson.append(data)
            data = {}

    elif db == "power_meter" :
        retrive = "Select no_device, volt, curr, power, unit, time from power_meter where token = ('" + tokens + "') and time >= ('" + curr_time + "') and time <= ('" + date_time + "');"
        #executing the quires
        cursor.execute(retrive)
        rows = cursor.fetchall()
        for row in rows :
            print(row)
            data = {'id': row[0], 'volt' : row[1], "curr" : row[2], "power" : row[3], "unit" : row[4], "time" : row[5].strftime("%Y-%m-%d %H:%M:%S")}
            # json_string = jsonify(data)
            myJson.append(data)
            data = {}

    #commiting the connection then closing it.
    connection.commit()
    connection.close()
    json_return = {tokens : myJson}
    json_string = jsonify(json_return)
    print(json_string)

    return json_string

# @app.route('/sendSME',methods=['post'])
# def sendSME():
#     j = request.get_json()
#     print(j)
#     print(j["token_id"])
#     json_val1 = j["token_id"]
#     json_val2 = j["temp"]
#     json_val3 = j["humid"]
#     #database connection
#     connection = pymysql.connect(host="localhost",user="root",passwd="rootsql@MoDiFy002",database="diprom_db" )

#     cursor = connection.cursor()
#     #insert = "INSERT INTO Sensor_data(token, temp, humid) VALUES(%s,%s,%s)",(j["token_id"],j["temp"],j["humid"]);"

#     # queries for retrievint all rows
#     retrive = "Select token from blynk_token where token in ('" +j["token_id"]+ "') and device in ('" + j["device"]+ "');"
#     #executing the quires
#     cursor.execute(retrive)
#     rows = cursor.fetchall()
#     # print(rows[0])
#     for row in rows :
#         data = row[0]

#     if data == j["token_id"] :
#         #executing the quires
#         cursor.execute("INSERT INTO Sensor_data(token, device, temp, humid) VALUES(%s,%s,%s,%s)",(j["token_id"],j["device"],j["temp"],j["humid"]))

#     #commiting the connection then closing it.
#     connection.commit()
#     connection.close()

#     return jsonify(j)

# @app.route('/gettoken',methods=['post'])
# def gettoken():
#     j = request.get_json()
#     # tokens = j["tokens"]

#     # token = tokens
#     #database connection
#     connection = pymysql.connect(host="localhost",user="root",passwd="rootsql@MoDiFy002",database="diprom_db" )

#     cursor = connection.cursor()
#     # queries for retrievint all rows
#     #retrive = "Select token, temp, humid  from Sensor_data WHERE " + j["tokens"] + " = token order by num desc;"
#     retrive = "Select blynk_token from blynk_token where token in ('" +j["tokens"]+ "') and device in ('" + j["device"]+ "');"
#     #executing the quires
#     cursor.execute(retrive)
#     rows = cursor.fetchall()
#     data = {}
#     # myJson = []
#     for row in rows :
#         print(row)
#         data = {'blynk_token': row[0]}
#         json_string = jsonify(data)
#         # myJson.append(data)
#         data = {}

#     #commiting the connection then closing it.
#     connection.commit()
#     connection.close()
#     # json_string = jsonify(myJson)
#     print(json_string)

#     return json_string

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='4006', use_reloader=True)
