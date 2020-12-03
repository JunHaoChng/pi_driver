#include <iostream>
#include "pi_driver.hpp"
#include "bcm2835.h"
#include "rclcpp/rclcpp.hpp"

using namespace std;

class Pi_driver
{
    public:
    Pi_driver()
    {
        cout<<"Hello world! One Pi driver coming up!";
        if (!bcm2835_init()) 
        {
            std::cout << "Initialization failed." << std::endl;
            std::cout << "Check if /dev/gpiomem permissions are correctly set."
                    << std::endl;
            exit(1);
        } 
        else
        {
            pin_setup();
            pwm_setup();
        }
    }
    void spin()
    {
        bcm2835_gpio_write(RPI_BPLUS_GPIO_J8_32, HIGH);
    }
    private:
    void pin_setup()
    {
        bcm2835_gpio_fsel(RPI_BPLUS_GPIO_J8_32, BCM2835_GPIO_FSEL_OUTP);
        bcm2835_gpio_write(RPI_BPLUS_GPIO_J8_32, HIGH);
        // bcm2835_gpio_set_pud(RPI_BPLUS_GPIO_J8_32, BCM2835_GPIO_PUD_DOWN);
    }

    void pwm_setup()
    {
        cout<<"Stuff";
    }  
};

int main()
{
    Pi_driver pi_d;
    while (true)
    {
        pi_d.spin();
        this_thread::sleep_for(std::chrono::milliseconds(200));
    }
    
	return 0;
}
