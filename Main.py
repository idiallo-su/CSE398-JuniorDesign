#MAIN CODE FINAL 

 

#!/usr/bin/env python 

# -*- coding: utf-8 -*- 

# 

#  test.py 

#   

#  Copyright 2022 rock <rock@rockpi-4b> 

#   

#  This program is free software; you can redistribute it and/or modify 

#  it under the terms of the GNU General Public License as published by 

#  the Free Software Foundation; either version 2 of the License, or 

#  (at your option) any later version. 

#   

#  This program is distributed in the hope that it will be useful, 

#  but WITHOUT ANY WARRANTY; without even the implied warranty of 

#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 

#  GNU General Public License for more details. 

#   

#  You should have received a copy of the GNU General Public License 

#  along with this program; if not, write to the Free Software 

#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, 

#  MA 02110-1301, USA. 

#   

#   

import mraa 
import time 
import sys 
import struct 
import binascii 

class DecodeError(Exception): 

    pass 
  

def _get_buffer_view(in_bytes): 

    mv = memoryview(in_bytes) 
    if mv.ndim > 1 or mv.itemsize > 1: 
        raise BufferError('object must be a single-dimension buffer of bytes.') 

    try: 
        mv = mv.cast('c') 
    except AttributeError: 
        pass 
      
    return mv 

  

def encode(in_bytes): 

    """Encode a string using Consistent Overhead Byte Stuffing (COBS). 
    Input is any byte string. Output is also a byte string. 
    Encoding guarantees no zero bytes in the output. The output 
    string will be expanded slightly, by a predictable amount. 
    An empty string is encoded to '\\x01'""" 

    if isinstance(in_bytes, str): 
        raise TypeError('Unicode-objects must be encoded as bytes first') 

    in_bytes_mv = _get_buffer_view(in_bytes) 

    final_zero = True 

    out_bytes = bytearray() 

    idx = 0 

    search_start_idx = 0 

    for in_char in in_bytes_mv: 

        if in_char == b'\x00': 

            final_zero = True 

            out_bytes.append(idx - search_start_idx + 1) 

            out_bytes += in_bytes_mv[search_start_idx:idx] 

            search_start_idx = idx + 1 

        else: 

            if idx - search_start_idx == 0xFD: 

                final_zero = False 

                out_bytes.append(0xFF) 

                out_bytes += in_bytes_mv[search_start_idx:idx+1] 

                search_start_idx = idx + 1 

        idx += 1 

    if idx != search_start_idx or final_zero: 

        out_bytes.append(idx - search_start_idx + 1) 

        out_bytes += in_bytes_mv[search_start_idx:idx] 

    return bytes(out_bytes) 

  

  

def decode(in_bytes): 

    """Decode a string using Consistent Overhead Byte Stuffing (COBS). 
    Input should be a byte string that has been COBS encoded. Output 
    is also a byte string. 
    A cobs.DecodeError exception will be raised if the encoded data 
    is invalid.""" 

    if isinstance(in_bytes, str): 
        raise TypeError('Unicode-objects are not supported; byte buffer objects only') 

    in_bytes_mv = _get_buffer_view(in_bytes) 
    out_bytes = bytearray() 
    idx = 0 

    if len(in_bytes_mv) > 0: 
        while True: 
            length = ord(in_bytes_mv[idx]) 
            
            if length == 0: 
                raise DecodeError("zero byte found in input") 
                
            idx += 1 
            end = idx + length - 1 
            copy_mv = in_bytes_mv[idx:end] 

            if b'\x00' in copy_mv: 
                raise DecodeError("zero byte found in input") 

            out_bytes += copy_mv 
            idx = end 

            if idx > len(in_bytes_mv): 
                raise DecodeError("not enough input bytes for length code") 

            if idx < len(in_bytes_mv): 
                if length < 0xFF: 
                    out_bytes.append(0) 
            else: 
                break 

    return bytes(out_bytes) 

  

# initialise UART 
uart = mraa.Uart("/dev/ttyS4") 
  
#set uart parameters 
uart.setBaudRate(9600) 
uart.setMode(8, mraa.UART_PARITY_NONE, 1) 
uart.setFlowcontrol(False, False) 
flag = 0 

while True: #flag == 0: 
  flag = 1 

  #if flag == 1: 

  encodedBytes = bytearray() 
  count = 0 

while True: 
  if uart.dataAvailable(100): 
    count += 1 
    data_byte = uart.read(1) 
    encodedBytes.extend(data_byte) 
    print(data_byte) 
    print(encodedBytes) 

    if count == 105: 
      break 

encodedBytesString = str(encodedBytes) 
print(encodedBytesString) 

exec(open("servo.py").read()) 

#----------------------------------------------------------------------------------------------------------------------------------------------------- 
#flag = 0 
# #reading from arduino 
# data_byte = uart.readStr(1).strip() 
# #encode 
# data_byte1 = data_byte.encode('utf-8') 
# #decode 
# data_byte2 = data_byte1.decode('ascii') 
# #prints 
# print(data_byte2.decode()) 
# uart.close() 
#test = decode(encodedBytes) 
#print(test) 
#print(encodedBytes.decode('utf8', 'strict')) 
