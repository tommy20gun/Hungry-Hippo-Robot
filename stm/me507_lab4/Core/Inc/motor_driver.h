/*
 * motor_driver.h
 *
 *  Created on: Apr 20, 2023
 *      Author: Ryan
 */

#ifndef INC_MOTOR_DRIVER_H_
#define INC_MOTOR_DRIVER_H_

#include "stm32f4xx_hal.h"

class motor_driver {
private:
    TIM_HandleTypeDef*  htim;
    uint32_t            ch1;
    uint32_t            ch2;
    uint8_t             direction;  // 0 = forward, 1 = reverse
    uint8_t 			polarity;

public:
    motor_driver(TIM_HandleTypeDef* _htim,
                 uint32_t _ch1,
                 uint32_t _ch2,
                 uint8_t _direction,
				 uint8_t _polarity);

    void enable_driver();
    void disable_driver();
    void set_duty_cycle(uint16_t dc);
    void set_direction(uint8_t direction);
};

#endif /* INC_MOTOR_DRIVER_H_ */
