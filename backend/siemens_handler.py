import snap7
from snap7.util import *

class MemoryWrapper:
    def __init__(self, name:str, db_num: int, start_addr: int) -> None:
        self.name = name
        self.db_num = db_num
        self.start_addr = start_addr
        
class DigitalMemoryWrapper(MemoryWrapper):
    def __init__(self, name:str, db_num: int, start_addr: int, bit_num: int) -> None:
        super().__init__(name, db_num, start_addr)
        self.bit_num = bit_num

class Device:
    def __init__(self, address: str, rack: int, slot: int) -> None:
        self.address = address
        self.rack = rack
        self.slot = slot
        self.client = snap7.client.Client()

    def write(self, area: object, db_number: int, start_address: int, value: bytearray) -> None:

        self.client.connect(self.address, self.rack, self.slot)
        self.client.write_area(area, db_number, start_address, value)
        self.client.disconnect()

    def read(self, area: object, db_number: int, start_address: int, length: int) -> int:

        self.client.connect(self.address, self.rack, self.slot)
        value = self.client.read_area(area, db_number, start_address, length)
        self.client.disconnect()
        return value

class S7_1200(Device):
    def __init__(self, address: str, rack: int, slot: int) -> None:
        super().__init__(address, rack, slot)

    def write_digital_output(self, db_number: int, start_address: int, value: bytearray) -> None:
        self.write(snap7.types.Areas.PA, db_number, start_address, value)
    
    def read_digital_output(self, db_number: int, start_address: int, length: int=1) -> bytearray:
        value = self.read(snap7.types.Areas.PA, db_number, start_address, length)
        return value
    
    def write_digital_input(self, db_number: int, start_address: int, value: bytearray) -> None:
        self.write(snap7.types.Areas.PE, db_number, start_address, value)
    
    def read_digital_input(self, db_number: int, start_address: int, length: int=1) -> bytearray:
        value = self.read(snap7.types.Areas.PE, db_number, start_address, length)
        return value
    
# plc = S7_1200('192.168.1.95', 0, 1)
# plc.write_digital_output(0, 0, bytearray([0x01]))
# print(plc.read_digital_output(0, 0, 1))