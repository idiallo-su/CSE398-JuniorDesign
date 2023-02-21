#DECODEDWRITETOWAVEFORMS CODE 
import mraa 
import time 
import sys 
import struct 
import binascii 

# initialize UART 
uart = mraa.Uart("/dev/ttyS4") 
#set uart parameters 
uart.setBaudRate(9600) 
uart.setMode(8, mraa.UART_PARITY_NONE, 1) 
uart.setFlowcontrol(False, False)  
inputStr = "b'z\x08\x00 \x00\x00\xb4=\x00\x00\x8c=\x00\x00\xa0=\x00\x00\xaa=\x00\x00\x96=\x00\x00\x82=\x00'" 
l = len(b'z\x08\x00 \x00\x00\xb4=\x00\x00\x8c=\x00\x00\xa0=\x00\x00\xaa=\x00\x00\x96=\x00\x00\x82=\x00') 

charBuffer = [] 
for i in range(l): 
charBuffer.append(inputStr[i]) 
print("Length output is: ", l) 
whatever = uart.write(bytearray(inputStr)) 
