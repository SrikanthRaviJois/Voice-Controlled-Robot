#include <WiFi.h>

const char *ssid = "tejusphone";
const char *password = "p@55w0rD";

int motor1Pin1 = 27; 
int motor1Pin2 = 26; 
int enable1Pin = 14;
int motor2Pin1 = 18;
int motor2Pin2 = 19;
int enable2Pin = 21;

const int freq = 30000;
const int pwmChannel1 = 0;
const int resolution = 8;
const int pwmChannel2 = 1;
int dutyCycle = 200;
int delayTime;

WiFiServer server(80);


//motor1 is Left motor
//motor2 is Right motor

void goRight(){
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, HIGH);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, HIGH);
  ledcWrite(pwmChannel1, dutyCycle);
  ledcWrite(pwmChannel2, 170);
}

void goLeft(){
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, HIGH);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, HIGH);
  ledcWrite(pwmChannel1, 170);
  ledcWrite(pwmChannel2, dutyCycle);
}

void goForward(){
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, HIGH);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, HIGH);
  ledcWrite(pwmChannel1, dutyCycle);
  ledcWrite(pwmChannel2, dutyCycle);
}

void comeBack(){
  digitalWrite(motor1Pin1, HIGH);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin1, HIGH);
  digitalWrite(motor2Pin2, LOW);
  ledcWrite(pwmChannel1, dutyCycle);
  ledcWrite(pwmChannel2, dutyCycle);
}

void stopCar(){
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, LOW);
}

void setup() {
  Serial.begin(115200);
  
  // Connect to Wi-Fi network
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  
  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());
  
  server.begin();

  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(enable1Pin, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(motor2Pin1, OUTPUT);
  pinMode(motor2Pin2, OUTPUT);
  pinMode(enable2Pin, OUTPUT);

  ledcSetup(pwmChannel1, freq, resolution);
  ledcAttachPin(enable1Pin, pwmChannel1);
  
  ledcSetup(pwmChannel2, freq, resolution);
  ledcAttachPin(enable2Pin, pwmChannel2);
}

void loop() {
  WiFiClient client = server.available();
  byte data[2];
  
  if (client) {
    while (client.connected()) {
      if (client.available()>=2) {
        client.read(data, 2);
        Serial.printf("%d\n", data[0]);
        delayTime = map(data[1], 0, 90, 0, 1465);
        
        if(data[0] == 1){
          goLeft();
          delay(delayTime);
          stopCar();
        }
        else if(data[0] == 2){
          goRight();
          delay(delayTime);
          stopCar();
        }
        else if(data[0] == 3){
          goForward();
        }
        else if(data[0] == 4){
          stopCar();
        }
        else if(data[0] == 5){
          comeBack();
        }
        // Process the received message as needed
      }
    }
    client.stop();
  }

  
}
