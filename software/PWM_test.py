from machine import Pin, PWM
import time

frequency = 2_000
duty_cycle = int((2**16)*0.2)
duty_cycle_l = 0
duty_cycle_h = duty_cycle
off_duty_cycle = int(2**16)

# bring V hight
# bring W low

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

def peliter(duty_cycle_f):
    duty_cycle = int(abs(duty_cycle_f)*(2**16))
    if(duty_cycle_f > 0):
        led_front.on()
        v_l.duty_u16(0)    # on
        w_l.duty_u16(off_duty_cycle)    #  off
        v_h.duty_u16(0)    # off
        w_h.duty_u16(duty_cycle)    # 
    elif(duty_cycle_f < 0):
        led_front.off()
        v_l.duty_u16(off_duty_cycle)    # off
        w_l.duty_u16(0)    # on
        v_h.duty_u16(duty_cycle) # on
        w_h.duty_u16(0)    # off
        
def fan(duty_cycle_f):
    duty_cycle = (2**16)-int(abs(duty_cycle_f)*(2**16))
    u_l.duty_u16(duty_cycle)    # on
    u_h.duty_u16(0)    # off
        

while True:
    time.sleep(2)           # sleep for 1 second
    peliter(0.95)
    fan(0.5)
    #u_l.duty_u16(duty_cycle_l)    # set 50% duty cycle, range 0-65535
    #v_l.duty_u16(duty_cycle_l)    # set 50% duty cycle, range 0-65535
    #w_l.duty_u16(duty_cycle_l)    # set 50% duty cycle, range 0-65535
    #u_h.deinit()           # turn off PWM on the pin
    #v_h.deinit()           # turn off PWM on the pin
    #w_h.deinit()           # turn off PWM on the pin
    #u_h.duty_u16(off_duty_cycle)    # set 50% duty cycle, range 0-65535
    #v_h.duty_u16(off_duty_cycle)    # set 50% duty cycle, range 0-65535
    #w_h.duty_u16(off_duty_cycle)    # set 50% duty cycle, range 0-65535

    time.sleep(2)           # sleep for 1 second
    #peliter(-0.2)
    #u_l.duty_u16(off_duty_cycle)    # set 50% duty cycle, range 0-65535
    #v_l.duty_u16(off_duty_cycle)    # set 50% duty cycle, range 0-65535
    #w_l.duty_u16(off_duty_cycle)    # set 50% duty cycle, range 0-65535
    #u_l.deinit()           # turn off PWM on the pin
    #v_l.deinit()           # turn off PWM on the pin
    #w_l.deinit()           # turn off PWM on the pin
    #u_h.duty_u16(duty_cycle_h)    # set 50% duty cycle, range 0-65535
    #v_h.duty_u16(duty_cycle_h)    # set 50% duty cycle, range 0-65535
    #w_h.duty_u16(duty_cycle_h)    # set 50% duty cycle, range 0-65535
    