/*
 * motor_driver.c
 *
 *  Created on: Apr 27, 2023
 *      Author: Ryan
 */

#include "motor_driver.h"

motor_driver::motor_driver(TIM_HandleTypeDef* _htim,
                           uint32_t _ch1,
                           uint32_t _ch2,
                           uint8_t _direction)
    :htim(_htim),
     ch1(_ch1),
     ch2(_ch2),
     direction(_direction)
{

}

void motor_driver::enable_driver() {
    HAL_TIM_PWM_Start(htim, ch1);
    HAL_TIM_PWM_Start(htim, ch2);
}

void motor_driver::disable_driver() {
    HAL_TIM_PWM_Stop(htim, ch1);
    HAL_TIM_PWM_Stop(htim, ch2);
}

void motor_driver::set_duty_cycle(uint16_t dc) {
    // forward
    if(direction == 0) {
        __HAL_TIM_SET_COMPARE(htim, ch1, dc);
        __HAL_TIM_SET_COMPARE(htim, ch2, 0);
    }
    // reverse
    else {
        __HAL_TIM_SET_COMPARE(htim, ch1, 0);
        __HAL_TIM_SET_COMPARE(htim, ch2, dc);
    }
}

void motor_driver::set_direction(uint8_t direction) {
    this->direction = direction;
}
