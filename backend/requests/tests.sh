curl -X POST http://localhost:5000/api/programm?ip=192.168.1.95&rack=0&slot=1&db=0&start_addr=0 \
     -H "Content-Type: application/json" \
     -d "$(cat requests/digital_output.json)"

curl -X GET "http://localhost:5000/api/digital/output?ip=192.168.1.95&rack=0&slot=1&db=0&start_addr=0"

curl -X POST "http://127.0.0.1:5000/api/digital/output?ip=192.168.1.95&rack=0&slot=1&db=0&start_addr=0&value=0,1,1,1"