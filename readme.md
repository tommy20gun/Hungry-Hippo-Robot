<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![MIT License][license-shield]][license-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/tommy20gun/Hungry-Hippo-Robot">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Hungry Hippo Robot</h3>

  <p align="center">
    The Hungry Hippo Robot project was a graduate level design term project for Cal Poly. We were tasked to build a robot to automously navigate an arena, pick up ping pong balls, and sort them based on color.
    <br />
    <a href="https://github.com/tommy20gun/Hungry-Hippo-Robot"><strong>Explore the docs »</strong></a>
    <br />
    <br />
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#Applications-used">Applications Used</a></li>
      </ul>
    </li>
    </li>
    <li><a href="#Mechanical-Design">Mechanical Design</a></li>
    <li><a href="#Electronic-Design">Electronic Design</a></li>
    <li><a href="#Software-Implementation">Software Implementation</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Product Name Screen Shot][coverpage]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Applications Used

* [![STM32CubeIDE][STM32CubeIDE]][STM32Cube-url]
* [![OpenCV][OpenCV]][OpenCV-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Mechanical Design -->
### Mechanical Design
<p align="right">(<a href="#readme-top">back to top</a>)</p>

Our design consists mainly of a large basket with the drive wheels, electronics,
and battery underneath. A pair of intake rollers, driven by a gear motor, bring
balls from the floor up into the basket. A ball wheel at the back of the basket
brings balls onto a shelf in a single file. Once a ball reaches the shelf, it
passes through the color sensor and then to the first servo. This servo either
knocks the ball back into the basket or allows it to continue rolling along the
shelf. If the ball continues along the shelf, it reaches the second servo, which 
directs the ball either into the shooter or out the back of the robot to drop
down into a corral or onto the floor of the arena.

During a match, the robot would first drive around picking up balls. The ball
wheel would be turning continuously so that balls are constantly moved through
the color sensor. Balls that match our designated color would be knocked back
into the basket to be deposited later. All other balls would be dropped out the
back of the robot back onto the arena. Once the robot has picked up enough balls
of our designated color, it would pass these balls either through the shooter to
put them into the cylinder in the center of the arena, or out the back of the
robot to drop them into our corral. Then the robot would start picking up balls
again and the cycle would repeat.

![Robot CAD][robot_cad]

<!-- Electronic Design -->
### Electronic Design

Wiring and wireless communication

The ambient light sensor is ADC and comes in a breakout board separate from the PCB. This is so that the board does not have to be placed where it is facing the floor to sense the line. The Color sensor will be I2C. Only 1 I2C “channel” needs to be activated. The Hall Sensor is GPIO.

We plan on wirelessly communicating with the robot with a Raspberry Pi. The motivation is just because we own a raspberry pi with Wi-Fi and can start testing SSH right away. It is important because all of our calculations for how to move the robot will be done on a computer running OpenCV in Python. The data sent to the motors will be serial data passed through SSH and into the UART of the Raspberry Pi where it can be received by the microcontroller with wired UART. I double checked that the Pi has alternate functions Rx and Tx.  

On the computer end, there will be a phone that will stream its camera feed into the computer, where OpenCV can capture and interpret the data. 

The custom PCB takes power from the 3S LiPo to power the robot. It uses a 5A switching regulator to supply 5V power to the Raspberry Pi and a 3A linear regulator to supply power to the microcontroller and sensors. The PCB has 5 motor outputs for the 2 drive motors, intake motor, ball wheel motor, and flywheel motor. Two of the motor connectors are duplicated in case we wanted to wire 2 motors to the same driver for the intake or flywheel. It also has 2 servo outputs and a hall sensor input. In addition, there are ports for communicating with the ST Link with UART6, communicating with the Raspberry Pi with UART1, and communicating with the color sensor via I2C. An extra header is connected to 9 unused pins on the microcontroller for extra functionality, and there are extra ports for supplying 3.3V, 5V, and 12V power. Lastly, there is a header connected to the motor driver inputs in case our microcontroller didn’t work and we had to attach a Blackpill instead.

![PCB][pcb]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Software Implementation -->
### Software Implementation

There are two major sections of code for the robot: the C++ code for the microcontroller, and python code for the computer and Raspberry Pi.

STM32IDE - C++
The C++ code uses a finite state machine in the main loop with 4 states.

State 0: Start state. In this state, the robot does nothing except wait for a signal to start. A GPIO interrupt triggered by the Raspberry PI (triggered by the user) brings the state machine to state 1.

State 1: The robot looks for a ball and moves towards it if it sees one. Here, the crux of the logic is inside the python scripts that were written for the robot. Here is where the UART1 Receive Interrupt is active. The robot will actively take motor duty cycle data given by the CPython program through UART1 to know how to drive itself. 
The only thing insde State 1 in the C++ code is to check the ADC reading of the light sensor. If the light reading falls below a certain threshold, the state machine will move into state 2. More on state 2 in the next section.
Video: https://photos.app.goo.gl/tfheLbLGFPe3WtNf7

State 2:  The purpose of state 2 is to correct the robot if it runs out of the arena. The light sensor actually has a good threshold value of 400 units that, when faced downward, determine if the robot is in the arena (where the floor is white) or outside of the arena (where the floor is grey). 
This is shown in a video demonstration where when we blast the light sensor with light, the state remains at 1. When the light sensor moves away from the light, the robot will go to state 2 and move backwards. 
Video: https://photos.app.goo.gl/UTSYJjyMzUb4Tg8u6 

State 3: This is the ball sorting state. Due to time constraints, we were not able to fully implement this portion of the robot. However, the color sensor and servos, as well as any motors function properly. One would only need to attach the ball carrier to make this work.
The color sensor is an I2C device that returns values of RGB based on what it sees. The code initializes all the necessary registers for I2C reading. Then the determineColor() function selects the RGB value with the biggest magnitude and determines the ball’s color based on the color with the biggest signal. For example, if blue = 1052, green = 870, red = 213, then the color was determined to be “Blue”.
The shortcoming of this algorithm was that it could not detect yellow balls, as yellow was a combination of blue and green. I wrote, but commented out, an algorithm where color values are compared to each other and then matched to a ratio, as all colors are just a ratio of RGB. This algorithm is good in theory but was not tested for accuracy. 
Color sensor part 1: https://photos.app.goo.gl/r2p6N2vRuNmkGFyi7  
Color sensor part 2: https://photos.app.goo.gl/Zmd4ECojo6uSsa898 

State 4: This is the Pause state. The sole purpose of this state is to act as the dead man’s switch. The code can be paused at any point in time where the user presses ‘Space Bar’ with the Python program opened. The computer would send an instruction to the Raspberry Pi that triggers a GPIO interrupt in the MCU to put the robot into its pause state. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

This portion of code took up the most time. However, I will not explain each class as it gets complicated quickly. I will only explain the logic of the Python code. 

![Opencvdemo][opencvdemo]

Within Cpython, the OpenCV Library is implemented. The order of logic is as follows. The camera detects Ball and Cart objects and sets the robot to spin in a circle until the front of the robot faces the ball. The code to make the robot spin in circle is M130M2CF.

When the robot faces the ball, then it will activate a proportional controller that drives it towards the ball to capture it. Further, if the robot is closer to the ball, the duty cycle will continuously decrease to 0 until the robot touches the ball. Since the ball was so close to the “cart”. The motor duty cycle was M1E and M2E. 0x0E is in hexadecimal. If there are no balls, the Python program will send an instruction to the Raspberry Pi to trigger an interrupt for the MCU to move the state machine into state 3.
The Camera is wirelessly connected to the CPython program through the IPcamera app on the phone. Distortion matrices were used to calibrate our camera. 
CPython is active at all times and sends motor duty cycle to the robot at all times, but the MCU makes it so that duty cycle data can control the robot ONLY in state 1. The program sends data to a Raspberry Pi hosting a server over iPV4 Wireless communication, which is a descriptive way of saying a Wifi Hotspot. Python’s socket class was used to allow this to function.

Raspberry Pi Python

The Raspberry Pi hosts a server on a Wifi Hotspot that allows any users to connect to it. Thus the camera, computer, and Raspberry Pi needed to be on the same network for this to work. The Pi opens a socket and the computer sends data over the socket. Then, the Raspberry Pi determines whether the data sent was a motor duty cycle, an instruction to pause, or an instruction to trigger state3. Once it deciphers this, it then sends the correct instruction to the MCU.

If it is a motor duty cycle, the Raspberry Pi encodes the string into UTF-8 format and sends the byte data over wired serial UART1 into the MCU. An interrupt is triggered on the MCU to read this data. IF the Pi receives a Pause instruction, a GPIO pin is toggled that triggers a different interrupt on the MCU to pause. Finally, if the Pi receives a State 3 instruction, another GPIO pin is toggled to trigger an interrupt on the MCU to move the program into state 3. 
The Raspberry Pi is the device that worked the most flawlessly. We were very lucky to not have to deal with RC or Bluetooth.

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE-MIT.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Tommy Xu tommy20gun00@gmail.com 

Ryan Ghosh rghosh776@gmail.com

Project Link: [https://github.com/tommy20gun/Hungry-Hippo-Robot](https://github.com/tommy20gun/Hungry-Hippo-Robot)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
* Charley Refvem: Prof. Mechanical Engineering
* [https://github.com/TemugeB/QR_code_orientation_OpenCV](https://github.com/TemugeB/QR_code_orientation_OpenCV)
* [https://realpython.com/python-sockets/](https://realpython.com/python-sockets/)
* [https://stackoverflow.com/questions/30032063/opencv-videocapture-lag-due-to-the-capture-buffer](https://stackoverflow.com/questions/30032063/opencv-videocapture-lag-due-to-the-capture-buffer)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/tommy20gun/Hungry-Hippo-Robot.svg?style=for-the-badge
[contributors-url]: https://github.com/tommy20gun/Hungry-Hippo-Robot/graphs/contributors
[license-shield]: https://img.shields.io/github/license/tommy20gun/Hungry-Hippo-Robot.svg?style=for-the-badge
[license-url]: https://github.com/tommy20gun/Hungry-Hippo-Robot/blob/master/LICENSE.txt
[product-screenshot]: images/screenshot.png
[robot_cad]: images/robot_cad.png
[pcb]: images/pcb.PNG
[STM32CubeIDE]:images/stm32cubeIDE.PNG
[STM32Cube-url]:https://www.st.com/en/development-tools/stm32cubeide.html
[OpenCV]:images/opencvlogo.PNG
[OpenCV-url]:https://opencv.org
[opencvdemo]:images/Opencvdemo.png
[coverpage]:images/coverpage.jpg