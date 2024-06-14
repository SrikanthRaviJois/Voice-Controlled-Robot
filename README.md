# Voice Controlled Robot Using ESP32 and Azure Speech to Text API
## Overview
This project demonstrates how to create a voice-controlled robot using an ESP32 microcontroller and Azure Speech to Text API. The ESP32 receives voice commands via Bluetooth or Wi-Fi, converts the spoken words to text using Azure Speech services, and controls the robot based on the recognized commands.

## Components
- ESP32 Microcontroller
- Motor driver (L298N or similar)
- DC motors and wheels
- Chassis for the robot
- Bluetooth module (optional)
- Power supply (Battery or USB)
- Azure Speech to Text API
- Arduino IDE 

## Prerequisites
- Basic knowledge of microcontrollers and programming
- Familiarity with Arduino IDE or PlatformIO
- Azure account to access Speech to Text API

## Setup Instructions
1. Hardware Assembly
    1. Chassis Assembly:

    - Attach the DC motors to the chassis.
    - Mount the wheels on the motors.

    2. Connect the Motor Driver:

    - Connect the motor driver inputs to the ESP32 GPIO pins.
    - Connect the motor driver outputs to the DC motors.

    3. Power Supply:
    - Connect the power supply to the motor driver and ESP32.

2. Software Setup
### ESP32 Setup
1. Install Arduino IDE:

    - Download and install the Arduino IDE from the official website.

2. Install ESP32 Board Package:

    - Open Arduino IDE.
    - Go to File -> Preferences.
    - In the "Additional Board Manager URLs" field, add: https://dl.espressif.com/dl/package_esp32_index.json.
    - Go to Tools -> Board -> Board Manager.
    - Search for "ESP32" and install the package.

### Azure Setup
1. Create Azure Speech Resource:
    - Sign in to the Azure portal.
    - Create a new Speech resource in the Azure portal.
    - Note the subscription key and region for the Speech resource.