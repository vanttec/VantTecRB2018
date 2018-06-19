
#include <Servo.h>
const int PIN_X8R_2 = A0;
const int PIN_X8R_5 = A2;
const int PIN_X8R_4 = A1; 

String inputString;

byte Thruster_left = 3;
byte Thruster_right = 5;
int rled = 11;
int bled = 12;
int gled = 13;


Servo left;
Servo right;

float channel4;
float channel5;
float channel2;

void setup() {
  left.attach(Thruster_left);
  right.attach(Thruster_right);

  pinMode(PIN_X8R_4, INPUT);
  pinMode(PIN_X8R_2, INPUT);
  pinMode(PIN_X8R_5, INPUT);
  pinMode(rled, OUTPUT);
  pinMode(bled, OUTPUT);
  pinMode(gled, OUTPUT);
  rgbon();
  left.writeMicroseconds(1500); // send "stop" signal to ESC.
  right.writeMicroseconds(1500); // send "stop" signal to ESC.
  Serial.begin(115200);
  delay(7000); // delay to allow the ESC to recognize the stopped signal
}

void loop() {
    read_values();
    select();
}
void read_values(){
    channel4 = pulseIn(PIN_X8R_4, HIGH);
    channel2 = pulseIn(PIN_X8R_2, HIGH);
    channel5 = pulseIn(PIN_X8R_5, HIGH);
  }

void select() {
  //Use channel 5 to select between manual or autonomous mode
  if (channel5 < 1300) {
    Serial.println(0);
    analogWrite(bled,255); 
     manual_Mode();
  }
  else if ( channel5 > 1600) {
    Serial.println(1);
    analogWrite(gled,255); 
    autonomous_Mode();
  }
  else {
      Serial.println(2);  
      analogWrite(rled,255); 
      right.writeMicroseconds(1500);
      left.writeMicroseconds(1500);
  }
}
void adelante(){
    int signal = 1700;
    left.writeMicroseconds(signal); // Send signal to ESC.
    right.writeMicroseconds(signal);
  }
  void atras(){
    int signal = 1300;
    left.writeMicroseconds(signal); // Send signal to ESC.
    right.writeMicroseconds(signal);
    }
  void girar_dere(){
    
    int signal = 1300;
    left.writeMicroseconds(signal); // Send signal to ESC.
    signal = 1700;
    right.writeMicroseconds(signal);
  }
  void girar_izq(){
    int signal = 1700;
    left.writeMicroseconds(signal); // Send signal to ESC.
    signal = 1300;
    right.writeMicroseconds(signal);
  }
  void manual_Mode() {
//void for manual movement
  float Y;
  float R;
  float L;

  if ((channel4 > 1450 & channel4 < 1550) & (channel2 > 1450 & channel2 < 1550)){     //Control stable
    int signal = 1500;
    left.writeMicroseconds(signal); // Send signal to ESC.
    right.writeMicroseconds(signal);   //thrusters at zero
    Serial.println('parado');
  }
  else if ((channel4 > 1450 & channel4 < 1550) & (channel2 < 1450 || channel2 > 1550)) {    //Control in advance
    int signal = map(channel2, 975, 2025, 1100, 1900);
    left.writeMicroseconds(signal); // Send signal to ESC.
    right.writeMicroseconds(signal);   //thrusters at zero
    Serial.println('enfrente');
  }
  else if ((channel4 < 1450 || channel4 > 1550) & (channel2 > 1450 & channel2 < 1550)) {    //Control for rotation both left and right
    int signal = map(channel4, 975, 2025, 1900, 1100);
    left.writeMicroseconds(signal); // Send signal to ESC.
    signal = map(channel4, 975, 2025, 1100, 1900);
    right.writeMicroseconds(signal);   //thrusters at zero
  }
  /*else if ((channel4 < 1450) & (channel2 < 1450 || channel2 > 1550)) {    //Control for turning left
    Y = (channel2-(channel2-1500)*(1500-channel4)/525);
    R = map(channel2, 975, 2025, 1100, 1900);
    L = map(Y, 975, 2025, 1100, 1900);
    thrusterRight.writeMicroseconds(R);
    thrusterLeft.writeMicroseconds(L);    //left thruster is proportionated for left turns
  }
  else if ((channel4 > 1550) & (channel2 < 1450 || channel2 > 1550)) {    //Control for turning right
    Y = (channel2-(channel2-1500)*(channel4-1500)/525);
    R = map(Y, 975, 2025, 1100, 1900);
    L = map(channel2, 975, 2025, 1100, 1900);
    thrusterRight.writeMicroseconds(R);
    thrusterLeft.writeMicroseconds(L);    //right thruster is proportionated for right turns
  }*/
}


void autonomous_Mode() {
  //void for autonomous navigation communicated via serial
  // put your main code here, to run repeatedly:
    // serial read section
    char c;
    
    while (Serial.available() > 0) {
        char c = Serial.read();
        inputString += c;  
        //wait for the next byte, if after this nothing has arrived it means 
        //the text was not part of the same stream entered by the user
        delay(1); 
    }
    
  //0123456789012
  //%B,1500,1500%
    if(inputString[0] == '%' && inputString.length() > 0 && inputString.length() < 14 && inputString[inputString.length() - 1] == '%' && inputString != ""){
      Serial.println(inputString);
      if(inputString[1] == 'B') {
          String valRight = inputString.substring(3,7);
          String valLeft = inputString.substring(8,12);
          //Serial.println(valLeft);
          int signal = valLeft.toInt();
          right.writeMicroseconds(signal);
          Serial.print(signal);
          signal = valRight.toInt();
          left.writeMicroseconds(signal);
          Serial.print(signal);
        }
        //Left thrusters
        else if(inputString[1] == 'L') {
          String valLeft = inputString.substring(3,7);
          //Serial.println(valLeft);
          int signal = valLeft.toInt();
          left.writeMicroseconds(signal); 
          Serial.print(signal);
        }
        //Right thrusters
        else if(inputString[1] == 'R') {
          String valRight = inputString.substring(3,7);
          //Serial.println(valRight);
          int signal = valRight.toInt();
          right.writeMicroseconds(signal);
          Serial.print(signal);
        }
    }  
    //Delete Previous Message
     inputString = "";
}
void rgbon(){
  analogWrite(rled,255); // Se enciende color rojo
  delay(500);            // Se esperan 500 ms
  analogWrite(rled,0);   // Se apaga color rojo 
  analogWrite(bled,255); // Se enciende color azul
  delay(500);            // Se esperan 500 ms
  analogWrite(bled,0);   // Se apaga color azul
  analogWrite(gled,255); // Se enciende color verde
  delay(500);            // Se esperan 500 ms
  analogWrite(gled,0);   // Se apaga colo verde
}

