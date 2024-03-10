from db import Watering_db
from siemens_handler import S7_1200
from time import sleep

db = Watering_db('watering', 'localhost', 5432, 'gardener', 'kap_kap_kap')
db.create_state_table()
# db.add_state_element("pole5")
# db.add_state_element("pole6")
# db.add_state_element("pole7")
plc = S7_1200('192.168.1.95', 0, 1)

while (True):
    try:
        states = plc.read_digital_output(0, 0, 1)
        states = states.to_bytes(6)
        db.update_state_element("pole5",states[0])
        db.update_state_element("pole6", states[1])
        db.update_state_element("pole7",states[2])
        print(db.get_states_list())
    except RuntimeError :
        print("device unrichable")
    
    sleep(1)
    
    