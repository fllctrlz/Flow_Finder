/*
 * Author: Ctrl-Z Robotics 
 * 
 * This program will be uploaded to the Arduino Uno
 * which is connected to the flow meter and the 
 * finger print sensor. Every 5 seconds, this program
 * will send data over the serial port to the fridge magnet.
 * The data includes the current user of the shower, (as
 * an ID based on the finger print), and the amount of 
 * water used in mL in the last 5 seconds. 
 */

#include <Adafruit_Fingerprint.h>
#include <SoftwareSerial.h>

int sensorInterrupt = 0; //this pin corresponds to aruino pin 2 
int flowSensorPin = 2; 
float sensorRate = 4.5;

volatile int pulseCount = 0;
float flowRate = 0.0;

long totalML = 0; 
long prevML = 0;
long deltaML = 0;
long prevDelta = 0;

long flowTime = 0;
long sendTime = 0;

int currentId = -1;

SoftwareSerial mySerial(3, 4); //green is 3, yellow is 4
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

void setup(){
  Serial.begin(9600);
  finger.begin(57600);
  pinMode(flowSensorPin, INPUT);
  digitalWrite(flowSensorPin, HIGH);
  attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
}

void loop(){
  /*
   * If there is no finger detected, look for a fingerPrint
   */
  if (currentId == -1){
    currentId = getFingerprintID();
  }
  /*
   * If 5 seconds has passed since the last time 
   * this section of code was executed, measure
   * and send the water usage in the last 5 seconds
   * to the fridge magnet
   */
  if((millis() - sendTime) > 5000){ 
      detachInterrupt(sensorInterrupt);
      sendTime = millis();
      //delta mL is the mL that have flowed in the past 5 seconds
      deltaML = totalML - prevML; 
      if ((prevDelta > 0) && (deltaML == 0)){
        currentId = -1;
      }
      sendData(currentId, deltaML);
      prevML = totalML;
      prevDelta = deltaML;
      attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
  }
  /*
   * Every second, calculate the mL
   * that have flowed through the flow sensor 
   * and add that to the total ML
   * 
   * The flow sensor pulses 4.5 times per second per litre/minute
   * So if the flow sends 4.5 pulses in the last second, 
   * we will know that the current flow rate is 1 litre/minute.
   * To calculate the mL that have flowed in the past second, 
   * we take the number of pulses in the last second from
   * the variable pulseCount, and divide that by 4.5 (sensorRate). 
   * We now have the flow rate in litres/minute. To convert that to mL/s
   * we divide the flow rate by 60 (since there are 60 seconds in one minute), 
   * and then multiply that by 1000 (since there are 1000 mL in one Litre).
   */
  if((millis() - flowTime) > 1000){
    flowRate = pulseCount/sensorRate; //flow rate in litres/minute
    totalML += (flowRate/60) * 1000;            
    pulseCount = 0;
    flowTime = millis();
  }
}

/*
 * Check for a finger, and if one is present 
 * return its ID
 */
int getFingerprintID() {
  uint8_t p = finger.getImage();
  if (p != FINGERPRINT_OK){
    return -1;   
  }

  p = finger.image2Tz();
  if (p != FINGERPRINT_OK){
    return -1;
  }

  p = finger.fingerFastSearch();
  if (p != FINGERPRINT_OK){
    return -1;
  }
  return finger.fingerID; 
}

void pulseCounter(){
  pulseCount++;
}

/*
 * Send the data to the fridge magnet
 * over the serial port
 */
void sendData(int id, int ml){
  Serial.print(id);
  Serial.print(" ");
  Serial.println(ml); 
}

