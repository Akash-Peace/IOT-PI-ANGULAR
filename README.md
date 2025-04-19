<p align="center">
  <img src="https://raw.githubusercontent.com/Akash-Peace/IOT-PI-ANGULAR/main/src/assets/agv_logo.png" alt="AGV Logo" width="150" height="150">
  <h3 align="center">Autonomous Guided Vehicle (AGV)</h3>
  <p align="center">
    <strong>A VIT College academic Project</strong>
    <br /><br />
    <a href="https://en.wikipedia.org/wiki/Internet_of_things"><strong>IoT</strong></a>
    .
    <a href="https://www.raspberrypi.org/"><strong>Raspberry Pi</strong></a>
    <br /><br />
    <a href="https://github.com/Akash-Peace/IOT-PI-ANGULAR/tree/main/Results">View Results</a>
    ·
    <a href="https://github.com/Akash-Peace/IOT-PI-ANGULAR/issues">Report Bug</a>
    ·
    <a href="https://github.com/Akash-Peace/IOT-PI-ANGULAR/issues">Request Feature</a>
  </p>
</p>

<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#built-with">Built With</a></li>
    <li><a href="#frontend-technology">Frontend Technology</a></li>
    <li><a href="#raspberry-pi-server">Raspberry Pi Server</a></li>
    <li><a href="#deployment-architecture">Deployment Architecture</a></li>
    <li><a href="#sensor-integration">Sensor Integration</a></li>
    <li><a href="#usage-guide">Usage Guide</a></li>
    <li><a href="#results">Results</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About The Project

Autonomous Guided Vehicle (AGV) is a smart remote-controlled vehicle powered by Raspberry Pi. It is designed to receive real-time commands from an Angular web interface, enabling precise control and automation. The system supports route recording, autonomous replay, reverse tracking, obstacle detection, line following, and weight sensing. This project is developed as part of an academic project at _VIT College_. [MIT](https://github.com/Akash-Peace/IOT-PI-ANGULAR/blob/main/LICENSE) licenses this project. If you find it useful, please consider giving it a _star_ and follow me!

## Features

- Real-time remote control via Angular frontend
- Route recording and auto-replay
- Reverse path traversal
- Line-following mode
- Weight sensing (HX711 load cell)
- Obstacle avoidance (Ultrasonic sensor)
- Buzzer-based alerts
- Persistent route saving

## Built With

* [Angular](https://angular.io/)
* [Python 3](https://www.python.org/)
* [WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
* [HX711 Load Cell](https://learn.sparkfun.com/tutorials/load-cell-amplifier-hx711-breakout-hookup-guide)
* [HC-SR04 Ultrasonic Sensor](https://components101.com/ultrasonic-sensor-working-pinout-datasheet)

## Frontend Technology

- Developed with Angular and TypeScript.
- WebSocket used for real-time bidirectional communication.
- Dynamic command dispatch for:
  - Forward, Backward, Left, Right, Stop
  - Start/Stop Route Recording
  - Route Replaying (Forward/Reverse)
  - Line Following
  - Emergency Halt
- User-friendly interface for selecting and executing saved routes.
- Auto-reconnect logic for WebSocket disconnection recovery.

## Raspberry Pi Server

- Implemented in Python 3 using `asyncio` and `websockets`.
- Controls motor direction and speed via PWM using GPIO.
- Reads weight from HX711 and distance from Ultrasonic sensor.
- Supports encoder-based distance tracking for precise automation.
- Background thread for continuous sensor monitoring and safety enforcement.
- Line-following logic using dual IR line sensors.

## Deployment Architecture

- Raspberry Pi acts as both:
  - **WebSocket server** on `ws://agv.local:8765`
  - **Motor controller + sensor processor**
- Angular app runs on any browser-enabled device on the same network.
- Angular-to-Pi interaction is handled purely via WebSocket messages.

## Sensor Integration

| Sensor         | Functionality                     |
|----------------|-----------------------------------|
| HX711          | Real-time weight sensing          |
| Ultrasonic     | Obstacle distance measurement     |
| IR Line Sensors| Line-following logic              |
| Rotary Encoder | Movement tracking (wheel rotation)|
| Buzzer         | Audio alerts                      |

## Usage Guide

1. Boot up Raspberry Pi and ensure it's on the same network.
2. Run the Angular app in a browser (use `ng serve` or host it).
3. Use control buttons to:
   - Drive manually (`F`, `B`, `L`, `R`, `S`)
   - Record paths
   - Replay or reverse saved routes
   - Activate line-following
4. Use `HALT` button anytime to safely stop automation.

## Results

View [results](https://github.com/Akash-Peace/IOT-PI-ANGULAR/tree/main/Results) here.

## License

Distributed under the MIT License. See [`LICENSE`](https://github.com/Akash-Peace/IOT-PI-ANGULAR/blob/main/LICENSE) for more details.

<!-- MY SYSTEM SPEC -->
## Development Environment

**OS:** [Ubuntu](https://ubuntu.com/)\
**System:** Customized PC\
**Processor:** Intel i5 13th gen\
**RAM:** DDR5 16GB\
**Disk:** NVMe 100GB

## Contact

Akash A\
Computer Science Engineer\
akashcse2000@gmail.com\
8608550403\
Chennai, TN, India

Follow me on

[<img src='https://github.com/Akash-Peace/INDUSTRIAL-WEBSITE/blob/main/images/linkedin.png' alt='linkedin' height='40'>](https://www.linkedin.com/in/akash-2000-cse) &nbsp; &nbsp; &nbsp; [<img src='https://github.com/Akash-Peace/INDUSTRIAL-WEBSITE/blob/main/images/instagram.png' alt='instagram' height='40'>](https://www.instagram.com/akash.a.2000) &nbsp; &nbsp; &nbsp; [<img src='https://github.com/Akash-Peace/INDUSTRIAL-WEBSITE/blob/main/images/facebook.png' alt='facebook' height='40'>](https://www.facebook.com/profile.php?id=100061841000593) &nbsp; &nbsp; &nbsp; [<img src='https://github.com/Akash-Peace/REACT-CHART-GENERATIVE-AI/blob/main/Test%20images/twitter.png' alt='twitter' height='40'>](https://twitter.com/AkashA53184506) &nbsp; &nbsp; &nbsp; [<img src='https://github.com/Akash-Peace/INDUSTRIAL-WEBSITE/blob/main/images/pypi.png' alt='pypi' height='50'>](https://pypi.org/user/Akash-Peace/) &nbsp; &nbsp; &nbsp; [<img src='https://github.com/Akash-Peace/INDUSTRIAL-WEBSITE/blob/main/images/youtube.png' alt='youtube' height='45'>](https://www.youtube.com/channel/UCmugCO6k7hgSZqaI1jzbelw/featured)
