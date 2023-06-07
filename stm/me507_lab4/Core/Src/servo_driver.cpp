/*
 * servo_driver.c
 *
 *  Created on: Apr 27, 2023
 *      Author: Ryan
 */

#include "servo_driver.h"

servo_driver::servo_driver(TIM_HandleTypeDef* _htim,
                           uint32_t _ch1)
    :htim(_htim),
     ch1(_ch1)
{

}

void servo_driver::enable_driver() {
    HAL_TIM_PWM_Start(htim, ch1);
}

void servo_driver::disable_driver() {
    HAL_TIM_PWM_Stop(htim, ch1);
}

void servo_driver::set_duty_cycle(uint16_t dc) {
    // forward
        __HAL_TIM_SET_COMPARE(htim, ch1, dc);
}
