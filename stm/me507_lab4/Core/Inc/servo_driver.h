/*
 * servo_driver.h
 *
 *  Created on: Apr 20, 2023
 *      Author: Ryan
 */

#ifndef INC_SERVO_DRIVER_H_
#define INC_SERVO_DRIVER_H_

#include "stm32f4xx_hal.h"

class servo_driver {
private:
    TIM_HandleTypeDef*  htim;
    uint32_t            ch1;

public:
    servo_driver(TIM_HandleTypeDef* _htim,
                 uint32_t _ch1);
    void enable_driver();
    void disable_driver();
    void set_duty_cycle(uint16_t dc);
};

#endif /* INC_MOTOR_DRIVER_H_ */
