def byteslist2bytearray(bytelist: str) -> bytearray:
    """ '0,1,1' to bytearray([0,1,1]) """
    byte_val = 0
    for i, byte in enumerate(bytelist.split(',')):
        byte_val += int(byte)*(2**i)
    return bytearray([byte_val])

def bytearray2byteslist(array: bytearray) -> str:
    """ bytearray([0,1,1]) to '0,1,1' """
    value = int.from_bytes(array)
    byteslist = ""
    while(value > 0):
        byteslist += str(value%2)
        value = int(value/2)
    return byteslist