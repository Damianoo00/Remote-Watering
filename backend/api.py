
from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin
from siemens_handler import S7_1200
import time
from utils import bytearray2byteslist, byteslist2bytearray
from db import ProgrammDB
app = Flask(__name__)
CORS(app)

# db = Watering_db('watering', 'localhost', 5432, 'gardener', 'kap_kap_kap')
app.logger.setLevel("INFO")
         
        
@app.route("/api/digital/output", methods=["OPTIONS"])
@cross_origin(supports_credentials=True)
def handle_options():
    response = make_response()
    response.headers["Access-Control-Allow-Origin"] = "*"  # Adjust origin as needed
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route("/api/digital/output", methods=["POST"])
def set_digital_output():
    query_params = request.args.to_dict()
    ip = str(query_params["ip"])
    rack = int(query_params["rack"])
    slot = int(query_params["slot"])
    db = int(query_params["db"])
    start_addr = int(query_params["start_addr"])
    value = byteslist2bytearray(query_params["value"])
    
    plc = S7_1200(ip, rack, 1)
    app.logger.info(f"Create S7-1200 device -> ip: [{ip}] | rack: [{rack}] | slot: [{slot}]")
    recived = False
    start = time.time()
    while (not recived):
        res = plc.write_digital_output(db,start_addr, value)
        app.logger.info(f"Write: db: [{db}] | start_addr: [{start_addr}] | value: [{value}] | res: [{res}]")
        time.sleep(0.001)
        curr_val = plc.read_digital_output(db, start_addr)
        app.logger.info(f"Read: db: [{db}] | start_addr: [{start_addr}] | curr_val: [{curr_val}]")
        if curr_val == value:
            recived = True
        if time.time() - start > 3:
            return 'Error Timeout', 500
    return {"value": bytearray2byteslist(value)}, 200
    
@app.route("/api/digital/output", methods=["GET"])
def get_digital_output():
    query_params = request.args.to_dict()
    ip = str(query_params["ip"])
    rack = int(query_params["rack"])
    slot = int(query_params["slot"])
    db = int(query_params["db"])
    start_addr = int(query_params["start_addr"])
    
    plc = S7_1200(ip, rack, 1)
    app.logger.info(f"Create S7-1200 device -> ip: [{ip}] | rack: [{rack}] | slot: [{slot}]")
    recived = False
    curr_val = plc.read_digital_output(db, start_addr)
    app.logger.info(f"Read: db: [{db}] | start_addr: [{start_addr}] | curr_val: [{curr_val}]")
        
    return {"value": bytearray2byteslist(curr_val)}, 200

@app.route("/api/programm", methods=["POST"])
def setup_programm():
    query_params = request.args.to_dict()
    ip = str(query_params["ip"])
    rack = int(query_params["rack"])
    slot = int(query_params["slot"])
    db = int(query_params["db"])
    start_addr = int(query_params["start_addr"])
        
    programm = request.json
    
    print(programm["programm"]["id"])
    
    db = ProgrammDB('watering', 'localhost', 5432, 'gardener', 'kap_kap_kap')
    # db.clear_tables()
    db.create_table()
    db.add_programm(programm["programm"])
    
    return "ok"