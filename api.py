from flask import Flask, request
from siemens_handler import S7_1200

app = Flask(__name__)
plc = S7_1200('192.168.1.95', 0, 1)

@app.route("/api/output/digital", methods=["GET", "POST"])
def handle_digital_output():
    body = request.json
    if request.method == "GET":
        value = plc.read_digital_output(int(body.get("db_number")), int(body.get("start_address")))
        return str(value)
    if request.method == "POST":
        plc.write_digital_output(int(body.get("db_number")), int(body.get("start_address")), bytearray([body.get("value")]))
    return "Done"
