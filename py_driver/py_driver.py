import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

from gpiozero import Motor
from gpiozero import PWMOutputDevice
import time

class Py_Driver(): 
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        print(self.kwargs)
        self.left_pwm = PWMOutputDevice(kwargs['left_pin'], kwargs['left_active_high'])
        self.left_motor = Motor(kwargs['left_forward'], kwargs['left_backward'],kwargs['left_pwm'])
        self.right_pwm = PWMOutputDevice(kwargs['right_pin'], kwargs['right_active_high'])
        self.right_motor = Motor(kwargs['right_forward'], kwargs['right_backward'],kwargs['right_pwm'])
    
    def test_motors(self):
        while(1):
            for i in range(0,6,1):
                i=(i+5)/10
                print(i)
                
                self.left_pwm.value = i
                self.left_motor.forward()
                self.right_pwm.value = i
                self.right_motor.forward()
                time.sleep(2.0)

                self.left_pwm.value = i
                self.left_motor.backward()
                self.right_pwm.value = i
                self.right_motor.backward()
                time.sleep(2.0)

    @property
    def move(self, linear_speed, angualr_speed, direction): # Use cmd_vel
        print("Getting movement")
        pass
        # Check that movement is consistent for both wheels, maybe with a scalar in the PWM.
    
    @move.setter
    def move(self, linear_speed, angular_speed):    # Speed is with respect to the front of the car
        print("Setting movement")

        print(linear_speed, angular_speed, move)
        pass

if __name__ == '__main__':
    # pi_d = Py_Driver(
    #     left_pin= 12,   left_active_high = True,          # left PWM settings 
    #     left_forward=16,left_backward=7, left_pwm=True,   # left Motor settings (using L298N)
    #     right_pin= 18,   right_active_high = True,          # right PWM settings 
    #     right_forward=14,right_backward=23, right_pwm=True,   # right Motor settings (using L298N)    
    # )

    # pi_d.test_motors()
    main()