import sys

## @brief BLE-Bin-CRC-Addition
# @Created: 11/6/2020
# @Author Robert Wood
# Opens a Cypress BLE binary file, and adds a four byte CRC to
# the end of the file then saves it with a name suitable for 
# for the OTA upgrade
# Commnd line arguments need to be the name of the file# to use and 
# the version number of the new verion in the format x.y.z
# eg snap40_shield-BCM920736TAG_Q32-rom-ram-Wiced-release.ota.bin
# and 1.4.12


WIDTH = 32 # CRC bit width
TOPBIT = 0x80000000
POLYNOMIAL = 0x04C11DB7

index = 0

##
# @fn def calculate_crc(new_version):
# @brief
# Calculates a CRC for the file input via the command line 
# @param[in] new_version - the verion of the new firmware
# ~param[in] previously created array of the specified input file
def calculate_crc(new_version,f_arr):
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
    new_file_name = "snap40_ble_V" + new_version + ".bin"
    newFile = open(new_file_name, "wb")
    pos = 0
    for byte in f_arr:
        newFile.write(f_arr[pos])
        pos += 1
    newFile.write((crc).to_bytes(4, byteorder='big'))
    newFile.close()


##
# @fn "Main" function of file
# @brief
# Reads in the file specified by sys.argv[1] and puts it into an array
# The array and sys.argv[2] is then passed to a function that calaulates 
# the crc and writes everything to a new file
n = len(sys.argv)
if n != 3:
    if n == 2:
        if sys.argv[1] != "-h" and sys.argv[1] != "-help":
            print("Invalid arguments. Input -h or ==help for help");
    print("Input the name of the file created by WICED")
    print("and the version number of the firmware in format x.y.z")
    print("eg. snap40_shield-BCM920736TAG_Q32-rom-ram-Wiced-release.ota.bin 1.2.66")       
else:        
    with open(sys.argv[1], "rb") as f:
        f_arr = []
        original_file = sys.argv[1]
        byte = f.read(1)
        while byte != b"": # Read every byte in the file...
            f_arr.append(byte) # ...and append it to an array
            index += 1
            byte = f.read(1)
        calculate_crc(sys.argv[2],f_arr)
    
        
        
      

