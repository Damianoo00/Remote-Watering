import logging
from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin
from siemens_handler import S7_1200, DigitalMemoryWrapper
from db import Watering_db
import threading
import json
import sys
from time import sleep
app = Flask(__name__)
CORS(app)

plc = S7_1200('192.168.1.95', 0, 1)
DQ1 = DigitalMemoryWrapper('DQ1',0,0,0)
DQ2 = DigitalMemoryWrapper('DQ2',0,0,1)
DQ3 = DigitalMemoryWrapper('DQ3', 0,0,2)

db = Watering_db('watering', 'localhost', 5432, 'gardener', 'kap_kap_kap')

@app.route("/api/digital/output", methods=["OPTIONS"])
@cross_origin(supports_credentials=True)
def handle_options():
    response = make_response()
    response.headers["Access-Control-Allow-Origin"] = "*"  # Adjust origin as needed
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route("/api/digital/output", methods=["GET", "POST"])
def handle_digital_output():  
    if request.method == 'GET':
        states = db.get_states_list()
        return {"value": json.dumps(states)}
    if request.method == 'POST':
        body = request.json 
        plc.write_digital_output(
            int(body.get("db_number")), 
            int(body.get("start_address")), 
            bytearray([body.get("value")]))
        return "Ok"
    

def record_states():
    db.clear_states() # dev
    db.create_state_table()
    db.add_state_element(DQ1.name)
    db.add_state_element(DQ2.name)
    db.add_state_element(DQ3.name)
    while (True):
        try:
            states = plc.read_digital_output(DQ1.db_num, DQ1.start_addr, 1)
            states = states.to_bytes(3)
            db.update_state_element(DQ1.name,states[DQ1.bit_num])
            db.update_state_element(DQ2.name, states[DQ2.bit_num])
            db.update_state_element(DQ3.name,states[DQ3.bit_num])
            print(db.get_states_list(), file=sys.stderr)
        except RuntimeError :
            print("device unrichable", file=sys.stderr)
        
        sleep(1)
        
watek = threading.Thread(target=record_states)
watek.start()