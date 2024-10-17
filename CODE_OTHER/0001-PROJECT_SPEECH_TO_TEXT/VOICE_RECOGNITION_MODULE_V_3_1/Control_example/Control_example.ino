int hey_noobix = 22;
int power_on = 23;
int turn_off = 24;
int set_timer = 25;
int give_infomration = 26;
int TIME = 27;
int temperature = 28;
int tell_joke = 29;
int how_are_you = 30;
int red = 31;
int green = 32;
int blue = 33;
int one_minute = 34;
int two_minutes = 35;
int three_minutes = 36;
int four_minutes = 37;
int five_minutes = 38;

bool HEY_NOOBIX = false;
bool POWER_ON = false;
bool TURN_OFF = false;
bool SET_TIMER = false;
bool GIVE_INFORMATION = false;
 
#include <SoftwareSerial.h>
#include "VoiceRecognitionV3.h"

VR myVR(10,11);    // 4:RX 5:TX, you can choose your favourite pins.

uint8_t records[7]; // save record
uint8_t buf[64];

int led = 13;

#define onRecord    (0)
#define offRecord   (1) 

/**
  @brief   Print signature, if the character is invisible, 
           print hexible value instead.
  @param   buf     --> command length
           len     --> number of parameters
*/
void printSignature(uint8_t *buf, int len)
{
  int i;
  for(i=0; i<len; i++){
    if(buf[i]>0x19 && buf[i]<0x7F){
      Serial.write(buf[i]);
    }
    else{
      Serial.print("[");
      Serial.print(buf[i], HEX);
      Serial.print("]");
    }
  }
}

/**
  @brief   Print signature, if the character is invisible, 
           print hexible value instead.
  @param   buf  -->  VR module return value when voice is recognized.
             buf[0]  -->  Group mode(FF: None Group, 0x8n: User, 0x0n:System
             buf[1]  -->  number of record which is recognized. 
             buf[2]  -->  Recognizer index(position) value of the recognized record.
             buf[3]  -->  Signature length
             buf[4]~buf[n] --> Signature
*/
void printVR(uint8_t *buf)
{
  Serial.println("VR Index\tGroup\tRecordNum\tSignature");

  Serial.print(buf[2], DEC);
  Serial.print("\t\t");

  if(buf[0] == 0xFF){
    Serial.print("NONE");
  }
  else if(buf[0]&0x80){
    Serial.print("UG ");
    Serial.print(buf[0]&(~0x80), DEC);
  }
  else{
    Serial.print("SG ");
    Serial.print(buf[0], DEC);
  }
  Serial.print("\t");

  Serial.print(buf[1], DEC);
  Serial.print("\t\t");
  if(buf[3]>0){
    printSignature(buf+4, buf[3]);
  }
  else{
    Serial.print("NONE");
  }
  Serial.println("\r\n");
}

void setup()
{
  /** initialize */
  myVR.begin(9600);  
  Serial.begin(115200);  
  if(myVR.clear() == 0){
    Serial.println("Recognizer cleared.");
  }
  else{
    Serial.println("Not find VoiceRecognitionModule.");
    Serial.println("Please check connection and restart Arduino.");
    while(1);
  }
  
  myVR.load(uint8_t (0));   //Hey noobix is saved on position 0
  


  pinMode(22, OUTPUT);
  pinMode(23, OUTPUT);
  pinMode(24, OUTPUT);
  pinMode(25, OUTPUT);
  pinMode(26, OUTPUT);
  pinMode(27, OUTPUT);
  pinMode(28, OUTPUT);
  pinMode(29, OUTPUT);
  pinMode(30, OUTPUT);
  pinMode(31, OUTPUT);
  pinMode(32, OUTPUT);
  pinMode(33, OUTPUT);
  pinMode(34, OUTPUT);
  pinMode(35, OUTPUT);
  pinMode(36, OUTPUT);
  pinMode(37, OUTPUT);
  pinMode(38, OUTPUT);

  digitalWrite(hey_noobix, LOW);
  digitalWrite(power_on, LOW);
  digitalWrite(turn_off, LOW);
  digitalWrite(set_timer, LOW);
  digitalWrite(give_infomration, LOW);
  digitalWrite(TIME, LOW);
  digitalWrite(temperature, LOW);
  digitalWrite(tell_joke, LOW);
  digitalWrite(how_are_you, LOW);
  digitalWrite(red, LOW);
  digitalWrite(green, LOW);
  digitalWrite(blue, LOW);
  digitalWrite(one_minute, LOW);
  digitalWrite(two_minutes, LOW);
  digitalWrite(three_minutes, LOW);
  digitalWrite(four_minutes, LOW);
  digitalWrite(five_minutes, LOW);
  

}

void loop()
{
  int ret;
  ret = myVR.recognize(buf, 50);
  if(ret>0){
    if(buf[1] == 0){
      turn_off_all();
      digitalWrite(hey_noobix, HIGH);
      HEY_NOOBIX = true;
      Serial.println("Hey Noobix");
      myVR.clear();                     //You must clear first the previous commands
      myVR.load(uint8_t (1));
      myVR.load(uint8_t (2));
      myVR.load(uint8_t (3));
      myVR.load(uint8_t (4));
    }


    if(HEY_NOOBIX){    
      if(buf[1] == 1){
        digitalWrite(power_on, HIGH);
        Serial.println("Power ON");
        POWER_ON = true;
        myVR.clear();
        myVR.load(uint8_t (9));
        myVR.load(uint8_t (10));
        myVR.load(uint8_t (11));
      }
  
      if(buf[1] == 2){
        digitalWrite(turn_off, HIGH);
        Serial.println("Turn OFF");
        TURN_OFF = true;
        myVR.clear();
        myVR.load(uint8_t (9));
        myVR.load(uint8_t (10));
        myVR.load(uint8_t (11));
      }

      if(buf[1] == 3){                              //Voice 3 is for "Set timer"
        digitalWrite(set_timer, HIGH);
        Serial.println("Set a timer for: ");
        SET_TIMER = true;
        myVR.clear();
        myVR.load(uint8_t (12));                     //Set timer to 1 minute
        myVR.load(uint8_t (13));                     //Set timer to 2 minutes
        myVR.load(uint8_t (14));                     //Set timer to 3 minutes
        myVR.load(uint8_t (15));                     //Set timer to 4 minutes
        myVR.load(uint8_t (16));                     //Set timer to 5 minutes
      }

      if(buf[1] == 4){                              //Voice 4 is for "Give information"
        digitalWrite(give_infomration, HIGH);
        Serial.println("Give information about: ");
        GIVE_INFORMATION = true;
        myVR.clear();
        myVR.load(uint8_t (5));                     //Information about time
        myVR.load(uint8_t (6));                     //Information about temperature
        myVR.load(uint8_t (7));                     //Information about telling a joke
        myVR.load(uint8_t (8));                     //Information about how are you
        
      }
    }
  

    if(POWER_ON){    
      if(buf[1] == 9){
        digitalWrite(red, HIGH);
        Serial.println("RED LED is ON");          
        turn_off_commands();
        myVR.clear();
        myVR.load(uint8_t (0));
      }
  
      else if(buf[1] == 10){
        digitalWrite(green, HIGH);
        Serial.println("GREEN LED is ON");          
        turn_off_commands();
        myVR.clear();
        myVR.load(uint8_t (0));
      }
  
      else if(buf[1] == 11){
        digitalWrite(blue, HIGH);
        Serial.println("BLUE LED is ON");          
        turn_off_commands();
        myVR.clear();
        myVR.load(uint8_t (0));
      }
    }

    if(TURN_OFF){    
      if(buf[1] == 9){
        digitalWrite(red, LOW);
        Serial.println("RED LED is OFF");          
        turn_off_commands();
        myVR.clear();
        myVR.load(uint8_t (0));
      }
  
      else if(buf[1] == 10){
        digitalWrite(green, LOW);
        Serial.println("GREEN LED is OFF");          
        turn_off_commands();
        myVR.clear();  
        myVR.load(uint8_t (0));
      }
  
      else if(buf[1] == 11){
        digitalWrite(blue, LOW);
        Serial.println("BLUE LED is OFF");         
        turn_off_commands();
        myVR.clear();
        myVR.load(uint8_t (0));
      }
    }


    if(SET_TIMER){    
      if(buf[1] == 12){
        digitalWrite(one_minute, HIGH);
        Serial.println("Timer set for 1 minute");          
        turn_off_commands();
        myVR.clear();
        myVR.load(uint8_t (0));
      }
  
      if(buf[1] == 13){
        digitalWrite(two_minutes, HIGH);
        Serial.println("Timer set for 2 minutes");          
        turn_off_commands();
        myVR.clear();
        myVR.load(uint8_t (0));
      }

      if(buf[1] == 14){
        digitalWrite(three_minutes, HIGH);
        Serial.println("Timer set for 3 minutes");          
        turn_off_commands();
        myVR.clear();
        myVR.load(uint8_t (0));
      }
      
      if(buf[1] == 15){
        digitalWrite(four_minutes, HIGH);
        Serial.println("Timer set for 4 minutes");          
        turn_off_commands();
        myVR.clear();
        myVR.load(uint8_t (0));
      }

      if(buf[1] == 16){
        digitalWrite(five_minutes, HIGH);
        Serial.println("Timer set for 5 minutes");          
        turn_off_commands();
        myVR.clear();
        myVR.load(uint8_t (0));
      }
      
    }


    if(GIVE_INFORMATION){
      if(buf[1] == 5){                                    //Voice 5 is for "Time"
        digitalWrite(TIME, HIGH);
        Serial.println("Time");          
        turn_off_commands();
        myVR.clear();
        myVR.load(uint8_t (0));
      }

      else if(buf[1] == 6){                               //Voice 6 is for "Temperature"
        digitalWrite(temperature, HIGH);
        Serial.println("Temperature");          
        turn_off_commands();
        myVR.clear();
        myVR.load(uint8_t (0));
      }

      else if(buf[1] == 7){                               //Voice 7 is for "Tell a joke"
        digitalWrite(tell_joke, HIGH);
        Serial.println("Telling a joke");          
        turn_off_commands();
        myVR.clear();
        myVR.load(uint8_t (0));
      }

      else if(buf[1] == 8){                               //Voice 8 is for "How are you"
        digitalWrite(how_are_you, HIGH);
        Serial.println("how are you");          
        turn_off_commands();
        myVR.clear();
        myVR.load(uint8_t (0));
      }
    }
    

    
    //Serial.println(buf[1]);
  }
}


void turn_off_commands(){
  POWER_ON = false;
  TURN_OFF = false;
  SET_TIMER =false;
  GIVE_INFORMATION = false;  
}


void turn_off_all(){
  digitalWrite(hey_noobix, LOW);
  digitalWrite(power_on, LOW);
  digitalWrite(turn_off, LOW);
  digitalWrite(set_timer, LOW);
  digitalWrite(give_infomration, LOW);
  digitalWrite(TIME, LOW);
  digitalWrite(temperature, LOW);
  digitalWrite(tell_joke, LOW);
  digitalWrite(how_are_you, LOW);
  //digitalWrite(red, LOW);
  //digitalWrite(green, LOW);
  //digitalWrite(blue, LOW);
  digitalWrite(one_minute, LOW);
  digitalWrite(two_minutes, LOW);
  digitalWrite(three_minutes, LOW);
  digitalWrite(four_minutes, LOW);
  digitalWrite(five_minutes, LOW);
}
