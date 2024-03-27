    #include <Servo.h>                // Use servo library
    Servo base, fArm, rArm, claw ;    // Create 4 servo objects
    
    // Store motor limits (const specifies the values as constants that cannot be changed during program execution)
    const int baseMin = 0;
    const int baseMax = 180;
    const int rArmMin = 45;
    const int rArmMax = 180;
    const int fArmMin = 35;
    const int fArmMax = 120;
    const int clawMin = 15;
    const int clawMax = 100;
    
    int DSD = 15; // Default Servo Delay (default motor movement delay)
                  // This variable controls the motor speed. Increasing it decreases the motor speed and thus controls the arm movement speed.
    
    void setup(){
      base.attach(2);     // Attach base servo to pin 2 with servo label 'b'
      delay(200);          // Stability wait
      rArm.attach(3);     // Attach rArm servo to pin 3 with servo label 'r'
      delay(200);          // Stability wait
      fArm.attach(4);      // Attach fArm servo to pin 4 with servo label 'f'
      delay(200);          // Stability wait
      claw.attach(11);      // Attach claw servo to pin 11 with servo label 'c'
      delay(200);          // Stability wait
    
      base.write(90); 
      delay(10);
      fArm.write(90); 
      delay(10);
      rArm.write(90); 
      delay(10);
      claw.write(90);  
      delay(10); 
    
      Serial.begin(9600); 
      Serial.println("Welcome to our Assistant Robot Arm");   
    }
    
    
    void loop(){
      if (Serial.available()>0) {  
        char serialCmd = Serial.read();
        armDataCmd(serialCmd);
      }
    }
    
    void armDataCmd(char serialCmd){ // Perform corresponding actions based on serial commands received by Arduino
                                    // Example commands: b45 (turn base to 45-degree angle)
                                    //                  o (output servo status information)
      if (serialCmd == 'b' || serialCmd == 'c' || serialCmd == 'f' || serialCmd == 'r'){
        int servoData = Serial.parseInt();
        servoCmd(serialCmd, servoData, DSD);  // Function to run servos of the robotic arm (parameters: servo name, target angle, delay/speed)
      } else {
        switch(serialCmd){    
          case 'o':  // Output servo status information
            reportStatus();
            break;
          default:  // Feedback for unknown commands
            Serial.println("Unknown Command.");
        }
      }  
    }
    
    void servoCmd(char servoName, int toPos, int servoDelay){  
      Servo servo2go;  // Create servo object
    
      // Serial monitor outputs received command information
      Serial.println("");
      Serial.print("+Command: Servo ");
      Serial.print(servoName);
      Serial.print(" to ");
      Serial.print(toPos);
      Serial.print(" at servoDelay value ");
      Serial.print(servoDelay);
      Serial.println(".");
      Serial.println("");  
      
      int fromPos; // Variable to store initial servo position
      
      switch(servoName){
        case 'b':
          if(toPos >= baseMin && toPos <= baseMax){
            servo2go = base;
            fromPos = base.read();  // Get current servo angle for initial position
            break;
          } else {
            Serial.println("+Warning: Base Servo Value Out Of Limit!");
            return;
          }
      
        case 'c':
          if(toPos >= clawMin && toPos <= clawMax){    
            servo2go = claw;
            fromPos = claw.read();  // Get current servo angle for initial position
            break;
          } else {
            Serial.println("+Warning: Claw Servo Value Out Of Limit!");
            return;        
          }
    
        case 'f':
          if(toPos >= fArmMin && toPos <= fArmMax){
            servo2go = fArm;
            fromPos = fArm.read();  // Get current servo angle for initial position
            break;
          } else {
            Serial.println("+Warning: fArm Servo Value Out Of Limit!");
            return;
          }
              
        case 'r':
          if(toPos >= rArmMin && toPos <= rArmMax){
            servo2go = rArm;
            fromPos = rArm.read();  // Get current servo angle for initial position
            break;
          } else {
            Serial.println("+Warning: rArm Servo Value Out Of Limit!");
            return;
          }      
      }
    
      // Command servo to move
      if (fromPos <= toPos){  // If initial position is less than target position
        for (int i=fromPos; i<=toPos; i++){
          servo2go.write(i);
          delay (servoDelay);
        }
      }  else { // If initial position is greater than target position
        for (int i=fromPos; i>=toPos; i--){
          servo2go.write(i);
          delay (servoDelay);
        }
      }
    }
    
    void reportStatus(){  // Servo status information
      Serial.println("");
      Serial.println("");
      Serial.println("+ Robot-Arm Status Report +");
      Serial.print("Claw Position: "); Serial.println(claw.read());
      Serial.print("Base Position: "); Serial.println(base.read());
      Serial.print("Rear  Arm Position:"); Serial.println(rArm.read());
      Serial.print("Front Arm Position:"); Serial.println(fArm.read());
      Serial.println("++++++++++++++++++++++++++");
      Serial.println("");
    }