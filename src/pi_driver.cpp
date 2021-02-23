#include <iostream>
#include <chrono>
#include <thread>
#include "pi_driver.hpp"
#include "bcm2835.h"
#include "rclcpp/rclcpp.hpp"

using std::cout;
using std::endl;
using namespace std::chrono_literals;

// PWM output on RPi Plug P1 pin 12 (which is GPIO pin 18)
// in alt fun 5.
// Note that this is the _only_ PWM pin available on the RPi IO headers
#define PIN RPI_BPLUS_GPIO_J8_32 
// and it is controlled by PWM channel 0
#define PWM_CHANNEL 0
// This controls the max range of the PWM signal
#define RANGE 1024

class Pi_driver : public rclcpp::Node
{
    public:
    Pi_driver() : Node("pi_driver")
    {
        cout<<"Hello world! One Pi driver coming up!"<<endl;
	if (!bcm2835_init())
	{
		cout<<"Initialization failed." <<endl;
		cout<<"Check if /dev/gpiomem permissiens are correctly set."<<endl;
            exit(1); 
	}
        else
        {
            pin_setup();
            //pwm_setup();
	    // spin();
	    RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Looping");
        }
    }
    void spin()
    {
        // Clock divider is set to 16.
        // With a divider of 16 and a RANGE of 1024, in MARKSPACE mode,
        // the pulse repetition frequency will be
        // 1.2MHz/1024 = 1171.875Hz, suitable for driving a DC motor with PWM
        bcm2835_pwm_set_clock(BCM2835_PWM_CLOCK_DIVIDER_16);
        bcm2835_pwm_set_mode(PWM_CHANNEL, 1, 1);
        bcm2835_pwm_set_range(PWM_CHANNEL, RANGE);

        // Vary the PWM m/s ratio between 1/RANGE and (RANGE-1)/RANGE
        // over the course of a a few seconds
        int direction = 1; // 1 is increase, -1 is decrease
        int data = 1;
        while (1)
        {
        if (data == 1)
            direction = 1;   // Switch to increasing
        else if (data == RANGE-1)
            direction = -1;  // Switch to decreasing
        data += direction;
        bcm2835_pwm_set_data(PWM_CHANNEL, data);
        bcm2835_delay(1);
	std::this_thread::sleep_for(200ms);
        }

        bcm2835_close();
    }
    private:
    void pin_setup()
    {
	// Set the output pin to Alt Fun 5, to allow PWM channel 0 to be output there
        bcm2835_gpio_fsel(PIN, BCM2835_GPIO_FSEL_ALT5);
        bcm2835_gpio_write(PIN, HIGH);
        std::this_thread::sleep_for(200ms);
	bcm2835_gpio_write(PIN, LOW);
 	std::this_thread::sleep_for(200ms);
        bcm2835_gpio_write(PIN, HIGH);
        std::this_thread::sleep_for(200ms);
	bcm2835_gpio_write(PIN, LOW);
 	std::this_thread::sleep_for(200ms);
    }

    void pwm_setup()
    {
        cout<<"Stuff";
    }  
};

int main(int argc, char* argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<Pi_driver>());
    rclcpp::shutdown();
    return 0;
}
