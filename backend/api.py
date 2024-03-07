from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin
from siemens_handler import S7_1200

app = Flask(__name__)
# plc = S7_1200('192.168.1.95', 0, 1)
CORS(app)

@app.route("/api/digital/output", methods=["OPTIONS"])
@cross_origin(supports_credentials=True)
def handle_options():
    response = make_response()
    response.headers["Access-Control-Allow-Origin"] = "*"  # Adjust origin as needed
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route("/api/digital/output", methods=["POST", 'OPTIONS'])
def handle_digital_output():
    body = request.json
    plc = S7_1200(
            body.get("ip_address"),
            body.get("rack_number"), 
            body.get("port_number")
            )
    response = make_response()
   
    if body.get("method") == "GET":
        value = plc.read_digital_output(
            int(body.get("db_number")), 
            int(body.get("start_address")))
        return {"value": value}
    if body.get("method") == "POST":
        plc.write_digital_output(
            int(body.get("db_number")), 
            int(body.get("start_address")), 
            bytearray([body.get("value")]))
        return "Ok"