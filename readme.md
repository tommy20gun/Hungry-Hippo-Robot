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
    <li><a href="#Mechanical-Design">Roadmap</a></li>
    <li><a href="#Electronic-Design">Contributing</a></li>
    <li><a href="#Software-Implementation">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Applications Used

* [![STM32CubeIDE][STM32Cube]][STM32Cube-url]
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
shelf. If the ball continues along the shelf, it reaches the second servo, which directs the ball either into the shooter or out the back of the robot to drop
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
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Software Implementation -->
### Software Implementation
<p align="right">(<a href="#readme-top">back to top</a>)</p>


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
[STM32CubeIDE]:
[STM32Cube-url]:https://www.st.com/en/development-tools/stm32cubeide.html
[OpenCV]:
[OpenCV-url]:https://opencv.org
