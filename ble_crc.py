import sys

WIDTH = 32
TOPBIT = 0x80000000
POLYNOMIAL = 0x04C11DB7

index = 0
f_arr = []

 
def calculate_crc():
    crc = 0xFFFFFFFF 
    print("From the function size is is %d",index)
    print("The first byte is %x and the last is %x",f_arr[0],f_arr[index-1])
    for y in range(0, index):
        bigvar = ord(f_arr[y])
        crc ^= (bigvar << (WIDTH - 8))
        crc &= 0xFFFFFFFF
        for z in range (0,8):
            if ((crc & TOPBIT) == TOPBIT):
                crc = (crc << 1) ^ POLYNOMIAL
            else:
                crc = (crc << 1)  
            crc &= 0xFFFFFFFF
                
    print ("The CRC is " , hex(crc))
    newFile = open("appended.bin", "wb")
    pos = 0
    for byte in f_arr:
        newFile.write(f_arr[pos])
        pos += 1
    newFile.write((crc).to_bytes(4, byteorder='big'))
 


with open("snap40ble_V1.0.0.bin", "rb") as f:
    byte = f.read(1)
    while byte != b"":
        f_arr.append(byte)
        index += 1
        byte = f.read(1)
    calculate_crc()
    
        
        
      

