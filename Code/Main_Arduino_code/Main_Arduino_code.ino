#include <AccelStepper.h>


// Motor Connections (unipolar motor driver)
const int In1 = 8;
const int In2 = 9;
const int In3 = 10;
const int In4 = 11;
// Motor Connections (constant voltage bipolar H-bridge motor driver)
const int AIn1 = 8;
const int AIn2 = 9;
const int BIn1 = 10;
const int BIn2 = 11;
// Motor Connections (constant current, step/direction bipolar motor driver)
const int dirPin = 2;
const int stepPin = 3;



String recievedMessage = "0";
AccelStepper myStepper(AccelStepper::DRIVER, stepPin, dirPin);

void setup() {
  Serial.begin(115200);

//  myStepper.setMaxSpeed(25000.0);
//  myStepper.setAcceleration(50000.0);
  myStepper.setMaxSpeed(20000.0);
  myStepper.setAcceleration(40000.0);
  //  myStepper.moveTo(atoi(recievedMessage));
  pinMode(13, OUTPUT);

}

void loop() {
  if (Serial.available()) {

    //  while (Serial.available() == 0) {
    //  }
    recievedMessage = Serial.readStringUntil('\n');
    int target = recievedMessage.toInt();
    if (target==1){
      digitalWrite(13, !digitalRead(13));
    }
    if (!myStepper.run()) {
      Serial.print("moving to ");
      Serial.println(target);
      
    }
//    myStepper.moveTo(target);
    if (target > 2500){ 
      target = 2500;
    }
    if (target < 10){ 
      target = 10;
    }
    myStepper.runToNewPosition(target);

  }
}
