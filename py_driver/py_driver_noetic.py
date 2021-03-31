#!/usr/bin/env python3
import rospy
# from rclpy.node import Node
from geometry_msgs.msg import Twist
from gpiozero import Motor
from gpiozero import PWMOutputDevice
import time
import numpy as np
import pprint

class Py_Driver():#Node): 
    def __init__(self, **kwargs):
        #super().__init__('py_driver')
        #self.subscription = self.create_subscription(Twist,'cmd_vel',self.listener_callback,0) # Store 10 messages, drop the oldest one
        #self.subscription  # prevent unused variable warning
        self.kwargs = kwargs
        # print(self.kwargs)

        self._left_pwm = PWMOutputDevice(kwargs['left_pin'], kwargs['left_active_high'])
        self._left_motor = Motor(kwargs['left_forward'], kwargs['left_backward'],kwargs['left_pwm'])
        self._right_pwm = PWMOutputDevice(kwargs['right_pin'], kwargs['right_active_high'])
        self._right_motor = Motor(kwargs['right_forward'], kwargs['right_backward'],kwargs['right_pwm'])
        print("Py Pi driver initialiased")

    def listener_callback(self, msg):
        # self.get_logger().info('Setting left & right wheel speed: %d %d' % (msg.linear.x, msg.angular.z))
        _move_dict = { 'linear':msg.linear.x,
            'angular':msg.angular.z}
        self.move = _move_dict

    def test_motors(self):
        # for i in range(0,6,1):
        # i=(i+5)/10
        # print(i)
        i = 0.6
        
        self._left_pwm.value = i
        self._left_motor.forward()
        self._right_pwm.value = i
        self._right_motor.forward()
        time.sleep(1.0)
        self._left_motor.stop()
        self._right_motor.stop()
   
    # Code relevant for tuning the left and right wheel movement
    @property
    def move(self):#, linear_speed, angular_speed): # Use cmd_vel
        print("Getting movement")
        return self._move
        # Check that movement is consistent for both wheels, maybe with a scalar in the PWM.
    
    @move.setter
    def move(self, _move_dict):    # Speed is with respect to the front of the car
        if (abs(_move_dict['linear']) > 0.5):
            _move_dict['linear'] = np.sign(_move_dict['linear']) * 0.5
            print("Movement constrained")
        if  (abs(_move_dict['angular']) > 1.0) :
            _move_dict['angular'] = np.sign(_move_dict['angular']) * 1.0
            print("Movement constrained")

        if (abs(_move_dict['linear']) <= 0.5 and _move_dict['angular']== 0.0) :
            print("Change")
            self._left_pwm.value =    abs(_move_dict['linear']/0.5)
            self._right_pwm.value =   abs(_move_dict['linear']/0.5)
            if np.sign(_move_dict['linear']) == 1:
                self._left_motor.forward()
                self._right_motor.forward()
            elif np.sign(_move_dict['linear']) == -1:
                self._left_motor.backward()
                self._right_motor.backward()
                print("Acts")
            print("Linear movement")

        elif (abs(_move_dict['linear']) == 0.0 and abs(_move_dict['angular']) >= 1.0) :
            self._left_pwm.value =    abs(_move_dict['angular']/1.0)
            self._right_pwm.value =   abs(_move_dict['angular']/1.0)
            if np.sign(_move_dict['angular']) == 1:
                self._left_motor.backward()
                self._right_motor.forward()
                print("Left wheel back, right wheel front")
            elif np.sign(_move_dict['angular']) == -1:
                self._left_motor.forward()
                self._right_motor.backward()
                print("Right wheel back, left wheel front")
            print("This bucket", (np.sign(_move_dict['angular']) == False))

        elif (abs(_move_dict['linear']) >= 0.5 and abs(_move_dict['angular']) >= 1.0) :
            if (np.sign(_move_dict['angular']) == 1 and np.sign(_move_dict['linear']) == 1):
                self._left_pwm.value =    0.5
                self._right_pwm.value =   1.0
                self._left_motor.forward()
                self._right_motor.forward()
            elif (np.sign(_move_dict['angular']) == -1 and np.sign(_move_dict['linear']) == 1):
                self._left_pwm.value =    1.0
                self._right_pwm.value =   0.5
                self._left_motor.forward()
                self._right_motor.forward()
            if (np.sign(_move_dict['angular']) == 1 and np.sign(_move_dict['linear']) == -1):
                self._left_pwm.value =    1.0
                self._right_pwm.value =   0.5
                self._left_motor.backward()
                self._right_motor.backward()
            elif (np.sign(_move_dict['angular']) == -1 and np.sign(_move_dict['linear']) == -1):
                self._left_pwm.value =    0.5
                self._right_pwm.value =   1.0
                self._left_motor.backward()
                self._right_motor.backward()

            print("Last bucket")
        
        else:
            self._left_pwm.value =  abs( (_move_dict['linear']/0.5 - _move_dict['angular']/1.0) / 2.0 )
            self._right_pwm.value = abs( (_move_dict['linear']/0.5 + _move_dict['angular']/1.0) / 2.0 )
            if (np.sign(_move_dict['linear']) == 1):
                self._left_motor.forward()
                self._right_motor.forward()
            elif (np.sign(_move_dict['linear']) == -1):
                self._left_motor.forward()
                self._right_motor.backward()
            print("Really the last bucket now")

        time.sleep(0.1)
        self._left_motor.stop()
        self._right_motor.stop()        

def main(args=None):
    #rclpy.init(args=args)
    rospy.init_node('py_driver', anonymous=False)
    
    # Hardcode for now, recommend to use a json file in the future
    py_driver = Py_Driver(
        left_pin= 12,      left_active_high = True,          # left PWM settings 
        left_forward=7,    left_backward=16, left_pwm=True,   # left Motor settings (using L298N)
        right_pin= 18,     right_active_high = True,          # right PWM settings 
        right_forward=14,  right_backward=23, right_pwm=True,   # right Motor settings (using L298N)
    )

    rospy.Subscriber("cmd_vel", Twist, py_driver.listener_callback)
    rospy.spin()
    # py_driver.test_motors()
    # rclpy.spin(py_driver)
    # rclpy.shutdown()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
