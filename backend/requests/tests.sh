curl -X POST http://localhost:5000/api/digital/output \
     -H "Content-Type: application/json" \
     -d "$(cat requests/digital_output.json)"

curl -X GET http://localhost:5000/api/digital/output \
     -H "Content-Type: application/json" \    
     -d "$(cat requests/digital_output.json)"