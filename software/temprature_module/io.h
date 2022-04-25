#define LED_front_pin 2
#define LED_blue_pin 25
#define LED_yellow_pin 22 // currently not working

#define U_L_pin 20
#define U_H_pin 17
#define V_L_pin 21
#define V_H_pin 18
#define W_L_pin 24
#define W_H_pin 19

#define OFF_DUTY_CYCLE pow(2,8)

#define thermistor_plate_pin 27
#define thermistor_heatsink_pin 26
#define thermistor_onboard_pin 4

extern float nominal_temprature;
// resistance at nominal temprature
extern float thermistor_nominal_plate;
extern float thermistor_nominal_heatsink;
