#include <Arduino.h>

int pinNumber = 13;

void setup() {
  // int frequency = 500;
    pinMode(pinNumber, OUTPUT); // Set the pin as output
    Serial.begin(9600); // Set the baud rate to 9600
}

void loop() {
    digitalWrite(pinNumber, HIGH); // Set the pin output to HIGH (1)
    Serial.println("Voltage: HIGH"); // Print the voltage level
    delay(500); // Wait for 500 milliseconds (0.5 seconds)
    digitalWrite(pinNumber, LOW); // Set the pin output to LOW (0)
    Serial.println("Voltage: LOW"); // Print the voltage level
    delay(500); // Wait for another 500 milliseconds (0.5 seconds)
}