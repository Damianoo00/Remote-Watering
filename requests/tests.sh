curl -X POST http://localhost:5000/api/output/digital \
     -H "Content-Type: application/json" \
     -d '{ "db_number": 0, "start_address": 0, "value": 0 }'

curl -X GET http://localhost:5000/api/output/digital \
     -H "Content-Type: application/json" \
     -d '{ "db_number": 0, "start_address": 0, "value": 0 }'