// FINAL CODE (ARDUINO TO ROCK PI) 

#include <Wire.h>  
#include <PacketSerial.h>  
#include <string> 

using namespace std;  

// Sample window width in mS (50 mS = 20Hz)  
const int sampleWindow = 50;   
unsigned int sample;   
float noiseData[21];

//string noiseData; 
string measurements = ""; 
int eventFlag = 11; 
boolean recordFlag = false; 

PacketSerial myPacketSerial;  

struct send_packet {  
  char header;  
  String measurements; 
};  

/************ SETUP ************ SETUP ************ SETUP ************/  
void setup(void) { 
  delay(100);  
  Serial.begin(9600);  
  Serial1.begin(9600);  
  Serial.println("Setup called");   

  Serial1.println("");  
  delay(100);  
  myPacketSerial.setStream(&Serial);  
  myPacketSerial.setStream(&Serial1);  
}  

/************ LOOP ************ LOOP ************ LOOP ************/  
void loop()   
{  
  unsigned long startMillis= millis();  // Start of sample window  
  unsigned int peakToPeak = 0;   // peak-to-peak level  
  unsigned int signalMax = 0;  
  unsigned int signalMin = 1024;    '
  
   // collect data for 50 mS  
   while (millis() - startMillis < sampleWindow) 
   {  
      sample = analogRead(0);  
      if (sample < 1024)  // toss out spurious readings  
      {  
         if (sample > signalMax)  
         {  
            signalMax = sample;  // save just the max levels  
         }  
         else if (sample < signalMin)  
         {  
            signalMin = sample;  // save just the min levels  
         }  
      }  
   }  
   
   peakToPeak = signalMax - signalMin;  // max - min = peak-peak amplitude  
   double volts = (peakToPeak * 5.0) / 1024;  // convert to volts  

   for (int i = 0; i < 20; i++) { 
      noiseData[i] = noiseData[i+1]; 
    } 
    noiseData[20] = volts; 
   delay(100);  

   //Our mic event  
   Serial.println(volts);  
   if(volts > 1) 
   {  
    Serial.println("Mic event detected!!");  
    //myPacketSerial.send((uint8_t*)&pkt, sizeof(pkt));  
    recordFlag = true; 
   }  
   //After event happens, start recording 
   if(recordFlag == true) { eventFlag--; } 

    //Once finished recording 
   if(eventFlag == 0) 
   { 
    send_packet pkt;  
    pkt.header = 'z';  
    Serial.print("z"); 
    Serial.print("\n"); 
    //Add measurements into packet 
    /* 
    for(int i=0; i<21; i++) {  
      pkt.measurements[i] = noiseData[i]; 
      Serial.print(" Measurement: ");  
      Serial.print(noiseData[i]);  
      Serial.println(" "); 
    } 
    */ 

    //Create string with the measurements 
    for(int i=0; i<21; i++) {  
      pkt.measurements += noiseData[i]; 
      pkt.measurements += ","; 
    } 

    Serial.println(pkt.measurements); 
    Serial.println("Sending packet!");  
    for (int i = 0; i < pkt.measurements.length(); i++){ 
      Serial1.print(pkt.measurements.charAt(i));   
    } 
    
    //myPacketSerial.send((uint8_t*)&pkt, sizeof(pkt)); 
    pkt.measurements = ""; 
    eventFlag = 11; 
    recordFlag = false; 
   } 
} 
