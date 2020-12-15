from gpiozero import Motor
from gpiozero import PWMOutputDevice
import time
   
def test_motors():
    front_motor = Motor(16, 7, pwm=True) # pwm is GPIO12
    back_motor = Motor(23, 15, pwm=True) # pwm is GPIO18 # GPIO23, 15 = 1.2, -1.88
    front_motor_pwm = PWMOutputDevice(12, True, 0, 1000)
    back_motor_pwm = PWMOutputDevice(18, True, 0, 1000)
    while(1):
        back_motor.forward(1.0)
        back_motor_pwm.value = 1.0
        front_motor.forward(1.0)
        front_motor_pwm.value = 1.0
    #front_motor.forward(1.0)
    #time.sleep(1)
    #front_motor.forward(0.5)
    #time.sleep(1)
    #front_motor.backward(0.5)
    #time.sleep(1)
    #front_motor.backward(1.0)
    #time.sleep(1) 

    #back_motor.forward(1.0)
    #time.sleep(1)
    #back_motor.forward(0.5)
    #time.sleep(1)
    #back_motor.backward(0.5)
    #time.sleep(1)
    #back_motor.backward(1.0)
    #time.sleep(1) 

def pin_setup(num_motors, pwm_pins, en_pins):
    return
def move(linear_speed, angualr_speed, direction):
    motor.forward()

if __name__ == '__main__':
    test_motors()

