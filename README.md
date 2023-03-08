# SoBot-Agri-Tech
 Programming example for SoBot to perform tasks using the Agri-Tech module and computer vision for decision making.


# Solis Robot - SoBot
![](https://github.com/SolisTecnologia/SoBot-Agri-Tech/blob/main/png/SoBotAgro.png)
# Introduction

AMR (autonomous mobile robotics) platform equipped with a camera system, ultrasonic and photoelectric sensors, works with a high rate of precision and repeatability of its movements, as it uses stepper motors in its movement and navigation, the SoBot also can be termed as a research and development interface, as it facilitates the practical experimentation of algorithms from the simplest to the most complex level.

This product was developed 100% by Solis Tecnologia, and has a lot of technology employing cutting-edge concepts, such as:

The motors can be controlled simultaneously or individually.
The user can select different accessories to implement to the robot.
Several programming languages can be used to connect via API.

# Components

* Main structure in aluminum
* Removable fairing with magnetic attachment points
* Robot Control Driver
* Agri-Tech Module
* Camera Webcam
* Raspberry Pi 4B board <img align="center" height="30" width="40" src="https://github.com/devicons/devicon/blob/master/icons/raspberrypi/raspberrypi-original.svg">
* 2x NEMA-23 Stepper Motors
* 2x 12V/5A battery

# Programming Example

 Programming example for SoBot to perform tasks using the Agri-Tech module and computer vision for decision making.

The application of the computer vision technique is used in this example to detect objects with specific chromatic characteristics, such as green and red, which can be associated, respectively, with healthy and diseased plants. When carrying out this identification, the programming triggers the liquid release system directed only to the plants diagnosed as sick, making the liquid application system precise and efficient.

### Programming Language

* Python  <img align="center" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg">


## Agri-Tech application - [Agri-Tech.py](https://github.com/SolisTecnologia/SoBot-Agri-Tech/blob/master/Agri-Tech.py)

### Required Libraries

~~~python
import serial
import cv2
import numpy as np
from time import time,sleep
from tracker import *
import threading
~~~

The ''serial'' library for serial/usb Raspberry connection with the robot controller driver.
The ''cv2'' library is used to apply the computer vision technique.
The "numpy" library is used with mathematical matrix functions
The ''time'' library is needed to generate time delays
The "tracker" library was developed to identify and track objects
The "threading" library is used to count timelines for triggering the liquid release system



## Agri-Tech application - [tracker.py](https://github.com/SolisTecnologia/SoBot-Agri-Tech/blob/main/tracker.py)

### Required Libraries

~~~python
import math
~~~

The ''math'' library is used to calculate trigonometric function




For more information about the commands used, check the Robot Commands Reference Guide.


# Reference Link
[SolisTecnologia website](https://solistecnologia.com/produtos/robotsingle)

# Please Contact Us
If you have any problem when using our robot after checking this tutorial, please contact us.

### Phone:
+55 1143040786

### Technical support email: 
contato@solistecnologia.com.br

![](https://github.com/SolisTecnologia/SoBot-Simple-Route/blob/master/png/logo.png)