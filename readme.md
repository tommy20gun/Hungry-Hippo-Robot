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
<h2 align="center">About This Project</h2>

---


<div id="image-table">
    <table>
	    <tr>
    	    <td style="padding:10px">
        	    <img src="images\robotworking.gif.gif" width="400"/>
      	    </td>
            <td style="padding:10px">
            	<img src="images\arena.png" width="200"/>
            </td>
        </tr>
    </table>
</div>
<!--![Product Name Screen Shot][coverpage]
![Product Name Screen Shot][back]-->



The Hungry Hippo Robot is a robot built to play a competitive game of Hungry Hippo in the arena(right). 
* The robot starts at its home-base
* The arena is scattered with ping pong balls
* The robot must collect then deposit the correct colored ball of it's home base color
* The robot must sort the ping pong balls, eliminating undesired colors
* The robot must deposit the balls in the center to earn 1 point





<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Applications Used

* [<img src="images/stm32cubeIDE.PNG" alt= “” width="50" height="25">][STM32Cube-url]
*  [<img src="images/opencvlogo.PNG" alt= “” width="50" height="25">][OpenCV-url]
*  [<img src="images/raspberrypi.png" alt= “” width="50" height="25">][raspberrypi-url]
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Mechanical Design -->
<h2 align="center">Mechanical Design</h2>

---


![Robot CAD][robot_cad]

<a href="https://github.com/tommy20gun/Hungry-Hippo-Robot"><strong>Explore the CAD » </strong> </a>

Our robot design features a large basket housing the drive wheels, electronics, and battery, with intake rollers bringing balls from the floor into the basket. A ball wheel on the back of the basket arranges the balls in a single file on a shelf. The balls then pass through a color sensor and a series of servos. If a ball matches the team color it continues rolling along the shelf, otherwise, it is knocked back into the basket. 

During a match, the robot drives around to collect balls, separating designated-color balls for later depositing and dropping the rest onto the arena. Once enough designated-color balls are collected, they are either shot into the arena center.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Electronic Design -->
<h2 align="center">Electrical Design</h2>

---
![PCB][pcb]

<a href="https://github.com/tommy20gun/Hungry-Hippo-Robot"><strong>Explore the eCAD » </strong> </a>

### Power
The custom PCB takes power from the 3S LiPo rechargable battery. Current passes through a 5A switching regulator to supply 5V power to the Raspberry Pi, and finally a 3A linear regulator to supply 3V3 power to the microcontroller and sensors. 
<p align="center">
  <img src="images/robotback.jpg" alt="" width="70%" height="70%">
</p>

### Features
* 5 motor outputs
* 2 servo outputs
* 9 microcontroller header pins
* Hall sensor input
* UART6 communication with the ST Link
* UART 1 communication with the Raspberry Pi
* I2C line
* Many extra JST connectors for 3.3V, 5V, and 12V power. 
* Emergency 10 Headers for motor input only  



### Sensors

* The ambient light sensor using ADC
* The color sensor using I2C
* Hall sensor using GPIO Input
* Kill Switch using GPIO External Interrupt triggered by Raspberry Pi





<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Software Implementation -->
<h2 align="center">Software Implmentation</h2>

---

### Wiring and wireless communication

The robot connects to a computer in 3 steps. First, we use UART to connect a Raspberry Pi to the MCU. The Raspberry Pi hosts a server, which a computer can connect to via Wifi Hotspot. This way, master control and emergency kill switch can come from a user controlling a computer. Also, we attached a wireless camera for OpenCV that must use the processing power of that computer.

There are two major sections of code for the robot: the C++ code for the microcontroller, and python code for the computer and Raspberry Pi.

STM32IDE - C++
The C++ code uses a finite state machine in the main loop with 4 states.

State 0: Start state. In this state, the robot does nothing except wait for a signal to start. A GPIO interrupt triggered by the Raspberry PI (triggered by the user) brings the state machine to state 1.

State 1: The robot looks for a ball and moves towards it if it sees one. Here, the crux of the logic is inside the python scripts that were written for the robot. Here is where the UART1 Receive Interrupt is active. The robot will actively take motor duty cycle data given by the CPython program through UART1 to know how to drive itself. 
The only thing insde State 1 in the C++ code is to check the ADC reading of the light sensor. If the light reading falls below a certain threshold, the state machine will move into state 2. More on state 2 in the next section.
![robotstate1][robotstate1]

State 2:  The purpose of state 2 is to correct the robot if it runs out of the arena. The light sensor actually has a good threshold value of 400 units that, when faced downward, determine if the robot is in the arena (where the floor is white) or outside of the arena (where the floor is grey). 
This is shown in a video demonstration where when we blast the light sensor with light, the state remains at 1. When the light sensor moves away from the light, the robot will go to state 2 and move backwards. 
![robotstate2][robotstate2]

State 3: This is the ball sorting state. Due to time constraints, we were not able to fully implement this portion of the robot. However, the color sensor and servos, as well as any motors function properly. One would only need to attach the ball carrier to make this work.
The color sensor is an I2C device that returns values of RGB based on what it sees. The code initializes all the necessary registers for I2C reading. Then the determineColor() function selects the RGB value with the biggest magnitude and determines the ball’s color based on the color with the biggest signal. For example, if blue = 1052, green = 870, red = 213, then the color was determined to be “Blue”.
The shortcoming of this algorithm was that it could not detect yellow balls, as yellow was a combination of blue and green. I wrote, but commented out, an algorithm where color values are compared to each other and then matched to a ratio, as all colors are just a ratio of RGB. This algorithm is good in theory but was not tested for accuracy. 

![bluecolorball][bluecolorball]
![redcolorball][redcolorball]

State 4: This is the Pause state. The sole purpose of this state is to act as the dead man’s switch. The code can be paused at any point in time where the user presses ‘Space Bar’ with the Python program opened. The computer would send an instruction to the Raspberry Pi that triggers a GPIO interrupt in the MCU to put the robot into its pause state. 
![pause][pause]

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
[raspberrypi-url]:https://www.raspberrypi.com
[opencvdemo]:images/Opencvdemo.png
[coverpage]:images/coverpage.jpg
[robotstate1]:images/robotworking.gif.gif
[robotstate2]:images/robotstate2.gif.gif
[bluecolorball]:images/colorsensor%20blue%20-%20Made%20with%20Clipchamp.gif
[redcolorball]:images/redball%20-%20Made%20with%20Clipchamp.gif
[pause]:images/pause.gif
[arena]:images/arena.PNG
[back]:images/robotback.jpg