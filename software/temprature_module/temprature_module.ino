/* temprature module controller */
// io.ino contains io handling
#include "io.h"

#define LED_front_pin 2
#define LED_blue_pin 25
#define LED_yellow_pin 22 // currently not working

void setup() {
  Serial.begin(9600);
  setup_io();
}

// the loop function runs over and over again forever
void loop() {
  float plate_temp = get_temprature(thermistor_plate_pin, thermistor_nominal_plate, nominal_temprature);
//  float plate_temp = getResistance(thermistor_plate_pin);
  Serial.print("plate temparture:");
  Serial.println(plate_temp);
  digitalWrite(LED_front_pin, HIGH);   // turn the LED on (HIGH is the voltage level)
  digitalWrite(LED_blue_pin, HIGH);   // turn the LED on (HIGH is the voltage level)
  digitalWrite(LED_yellow_pin, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);                       // wait for a second
  digitalWrite(LED_front_pin, LOW);    // turn the LED off by making the voltage LOW
  digitalWrite(LED_blue_pin, LOW);    // turn the LED off by making the voltage LOW
  digitalWrite(LED_yellow_pin, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);                       // wait for a second
}
