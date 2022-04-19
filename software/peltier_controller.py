from machine import Pin, PWM
import machine
import time
import math
import utime

plate_setpoint = 10
heatsink_setpoint = 24
tick = 200
adc_period = 10

frequency = 2_000
off_duty_cycle = int(2**16)

# Thermistor
R1 = 10e3
thermistor = 33e3
#voltage = 3.3*(adc/(2**16))
#thermsitor = R/(3.3/V-1)
#thermistor = R/(2**16/adc-1)
#thermistor = R.adc/(2**16-adc)
thermistor_plate_pin = machine.ADC(27)
thermistor_heatsink_pin = machine.ADC(26)
thermistor_onboard = machine.ADC(4)

#TODO save these constants to flash
if(False):
    nominal_temprature = 20
    # resistance at nominal temprature
    thermistor_nominal_plate = 35300
    thermistor_nominal_heatsink = 37000
elif(True):
    nominal_temprature = 18.8
    # resistance at nominal temprature
    thermistor_nominal_plate = 8725
    thermistor_nominal_heatsink = 11430
# The beta coefficient of the thermistor (usually 3000-4000)
BCOEFFICIENT = 3950

# Output config
led_front = Pin(2, Pin.OUT)    # create output pin on GPIO0
u_l = PWM(Pin(20))      # create PWM object from a pin
u_l.freq(frequency)         # set frequency
v_l = PWM(Pin(21))      # create PWM object from a pin
v_l.freq(frequency)         # set frequency
w_l = PWM(Pin(24))      # create PWM object from a pin
w_l.freq(frequency)         # set frequency

u_h = PWM(Pin(17))      # create PWM object from a pin
u_h.freq(frequency)         # set frequency
v_h = PWM(Pin(18))      # create PWM object from a pin
v_h.freq(frequency)         # set frequency
w_h = PWM(Pin(19))      # create PWM object from a pin
w_h.freq(frequency)         # set frequency

def getResistance(adc, R=R1):
    val = adc.read_u16()
    resistance = R*val/(2**16-val) # calculate the resistance
    return resistance

def getTemprature(adc, thermistorNominal, R=R1):
    # from https://learn.adafruit.com/thermistor/using-a-thermistor
    resistance = getResistance(adc, R=R)
    steinhart = resistance / thermistorNominal  # (R/Ro)
    steinhart = math.log(steinhart)                  # ln(R/Ro)
    steinhart /= BCOEFFICIENT                   # 1/B * ln(R/Ro)
    steinhart += 1.0 / (nominal_temprature + 273.15) # + (1/To)
    steinhart = 1.0 / steinhart                 # Invert
    steinhart -= 273.15                         # convert absolute temp to C
    #return resistance
    return steinhart 

def peliter(duty_cycle_f):
    duty_cycle = int(abs(duty_cycle_f)*(2**16))
    if(duty_cycle_f > 0):
        # cool peliter
        # v at GND w at VCC
        led_front.on()
        v_l.duty_u16(0)              # on
        w_l.duty_u16(off_duty_cycle) # off
        v_h.duty_u16(0)              # off
        w_h.duty_u16(duty_cycle)     # on
    elif(duty_cycle_f < 0):
        # heat peliter
        # v at VCC w at GND
        led_front.off()
        v_l.duty_u16(off_duty_cycle) # off
        w_l.duty_u16(0)              # on
        v_h.duty_u16(duty_cycle)     # on
        w_h.duty_u16(0)              # off
        
def fan(duty_cycle_f):
    duty_cycle = (2**16)-int(abs(duty_cycle_f)*(2**16))
    u_l.duty_u16(duty_cycle) # on
    u_h.duty_u16(0)          # off
    
def PI_controller(measured, setpoint, integral, P=0.2, I=0, integral_cap = 0.2, pwm_min = 0):
    temp_error = setpoint-measured
    integral += temp_error*I
    integral = max(min(integral_cap, integral), -integral_cap)
    output = temp_error*P+integral
    output = max(min(0.95, output), -0.95)
    return output, integral

def update_command(comand_str, cur_temp):
    """ update settings and write to file """
    global temp_offset, temprature
    f = open("settings.txt", "wb")
    settings_list = []
    if(comand_str[:2] == "T:"):
        read_float = float(comand_str[2:])
        print("read:%f", read_float)
        temp_offset += read_float-cur_temp
        settings_bytes = ustruct.pack(settings_format, temp_offset)
        f.write(settings_bytes)
        f.close()
    else:
        print("Did not unsertand comand : %s", comand_str)


temp_plate = getTemprature(thermistor_plate_pin, thermistor_nominal_plate)
temp_heat  = getTemprature(thermistor_heatsink_pin, thermistor_nominal_heatsink)
last_update_adc = 0
last_update = 0
fan_integral = 0

while True:
    cur_time = utime.ticks_ms()
    
    # read adc
    if(cur_time - last_update_adc > adc_period):
        last_update_adc = cur_time
        temp_plate_n = getTemprature(thermistor_plate_pin, thermistor_nominal_plate)
        temp_heat_n = getTemprature(thermistor_heatsink_pin, thermistor_nominal_heatsink)
        temp_plate = 0.5*temp_plate_n+0.5*temp_plate
        temp_heat  = 0.5*temp_heat_n +0.5*temp_heat
        
    if(cur_time - last_update > tick):
        last_update = cur_time
        print(f"plate:{temp_plate:.2f}\theatsink:{temp_heat:.2f}")
        fan_out, fan_integral = PI_controller(temp_plate, plate_setpoint, fan_integral)
        peliter(0.98)
        # simplistic pi controller for the fan
        fan_out, fan_integral = PI_controller(temp_heat, heatsink_setpoint, fan_integral)
        fan(0.95)
        #time.sleep(2)           # sleep for 1 second
