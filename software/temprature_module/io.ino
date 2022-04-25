#include <math.h>
#include "io.h"


#define R1 10e3
#define thermistor 33e3

float nominal_temprature = 18.8;
// resistance at nominal temprature
float thermistor_nominal_plate = 35.3e3;
float thermistor_nominal_heatsink = 35.3e3;
// The beta coefficient of the thermistor (usually 3000-4000)
const float BCOEFFICIENT = 3950;


void setup_io(){
  pinMode(LED_front_pin, OUTPUT);
  pinMode(LED_blue_pin, OUTPUT);
  pinMode(LED_yellow_pin, OUTPUT);
  analogWriteResolution(8);
}

void peliter(float duty_cycle_f){
  int duty_cycle = int(abs(duty_cycle_f)*(OFF_DUTY_CYCLE));
  analogWrite(U_H_pin, 128);
  analogWrite(U_L_pin, 255);
  analogWrite(V_H_pin, 0);
  analogWrite(V_L_pin, 0);
  if(duty_cycle_f > 0){
    // cool peliter
    // v at GND w at VCC
    analogWrite(V_L_pin, 0);              // on
    analogWrite(V_H_pin, 0);              // off
    analogWrite(W_L_pin, OFF_DUTY_CYCLE); // off
    analogWrite(W_H_pin, duty_cycle);     // on
  }else if(duty_cycle_f < 0){
    // heat peliter
    // v at VCC w at GND
    analogWrite(V_L_pin, OFF_DUTY_CYCLE); // off
    analogWrite(V_H_pin, duty_cycle);     // on
    analogWrite(W_L_pin, 0);              // on
    analogWrite(W_H_pin, 0);              // off
  }
}

void fan(float duty_cycle_f){
  int duty_cycle = OFF_DUTY_CYCLE-int(abs(duty_cycle_f)*(OFF_DUTY_CYCLE));
  analogWrite(U_H_pin, 0);          // off
  analogWrite(U_L_pin, duty_cycle); // on
}

float getResistance(int analogPin){
  float val = analogRead(analogPin);
  float resistance = R1*val/(pow(2, 10)-val); // calculate the resistance
  return resistance;
}

float get_temprature(int adc_pin, float thermistorNominal, float nominal_temprature_in){
    // from https://learn.adafruit.com/thermistor/using-a-thermistor
    float resistance = getResistance(adc_pin);
    float steinhart = resistance / thermistorNominal;  // (R/Ro)
    steinhart = log(steinhart);             // ln(R/Ro)
    steinhart /= BCOEFFICIENT;                   // 1/B * ln(R/Ro)
    steinhart += 1.0 / (nominal_temprature_in + 273.15); // + (1/To)
    steinhart = 1.0 / steinhart;                 // Invert
    steinhart -= 273.15;                         // convert absolute temp to C
    return steinhart;
}
