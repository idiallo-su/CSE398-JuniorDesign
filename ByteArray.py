#BYTEARRAY REMOVAL CODE  
#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# 
#  bytearrayremoval.py 
#   
#  Copyright 2022 rock <rock@rockpi-4b> 
#  
#   
encodedBytesString = "bytearray(b'0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.07,0.11,0.46,4.97,0.11,2.83,0.22,1.06,0.07,0.07,0.07,0.07,0.07,0.07,')" 
newEncodedBytesString = encodedBytesString[12:len(encodedBytesString)-3].split(",") 
cleanedEncodedBytesString = [] 
for string in newEncodedBytesString: 
cleanedEncodedBytesString.append(float(string)) 
print(newEncodedBytesString) 
print(cleanedEncodedBytesString) 
