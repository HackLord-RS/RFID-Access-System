#include <Wire.h>
#include <RTClib.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

LiquidCrystal_I2C lcd(0x27, 20, 4);
RTC_DS1307 rtc;
#define greenLED 12
#define redLED 13
#define servoPin 11

Servo myServo;

struct User {
  String tag_id;
  String name;
  String phone;
};

User users[6] = {
  {"231678", "Anushka", "9452481810"},
  {"231694", "Kanisha", "9350982281"},
  {"221711", "Sathwik", "9032609979"},
  {"231696", "Anji", "6300759994"},
  {"231697", "Kunal", "8305762078"},
  {"231699", "Manita", "7849983155"}
};

String enteredID;

void setup() {
  Serial.begin(9600);

  lcd.init();
  lcd.backlight();

  if (!rtc.begin()) {
    Serial.println("RTC not found!");
    while (true);
  }
  if (!rtc.isrunning()) {
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }

  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);
  myServo.attach(servoPin);
  myServo.write(0); 

  lcd.setCursor(2, 0);
  lcd.print("RFID ACCESS SYSTEM");
  lcd.setCursor(3, 2);
  lcd.print("Enter Your ID:");
}

void loop() {
  if (Serial.available()) {
    Serial.println("Enter the unique ID: ");
    enteredID = Serial.readStringUntil('\n'); 
    enteredID.trim(); 
    checkAccess();
  }
}

void checkAccess() {
  bool found = false;
  String userName, userPhone;

  for (int i = 0; i < 6; i++) {
    if (enteredID == users[i].tag_id) {
      found = true;
      userName = users[i].name;
      userPhone = users[i].phone;
      break;
    }
  }

  DateTime now = rtc.now();
  String timestamp = String(now.hour()) + ":" + String(now.minute()) + ":" + String(now.second());

  lcd.clear();

  if (found) {
    digitalWrite(greenLED, HIGH);
    digitalWrite(redLED, LOW);
    myServo.write(90); 

    Serial.println("\n✅ ACCESS GRANTED ✅");
    Serial.println("Name: " + userName);
    Serial.println("Phone: " + userPhone);
    Serial.println("Timestamp: " + timestamp);

    lcd.setCursor(2, 0);
    lcd.print("✅ ACCESS GRANTED!");
    lcd.setCursor(2, 1);
    lcd.print("Name: " + userName);
    lcd.setCursor(2, 2);
    lcd.print("Phone: " + userPhone);
    lcd.setCursor(2, 3);
    lcd.print("Time: " + timestamp);

    delay(5000);
    myServo.write(0); 
    digitalWrite(greenLED, LOW);
  } else {
    digitalWrite(greenLED, LOW);
    digitalWrite(redLED, HIGH);

    Serial.println("\n❌ ACCESS DENIED ❌");
    Serial.println("Invalid ID!");

    lcd.setCursor(2, 0);
    lcd.print("❌ ACCESS DENIED!");
    lcd.setCursor(2, 1);
    lcd.print("Invalid ID!");

    delay(3000);
    digitalWrite(redLED, LOW);
  }

  lcd.clear();
  lcd.setCursor(3, 0);
  lcd.print("Enter Your ID:");
}
