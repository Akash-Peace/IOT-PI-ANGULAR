import RPi.GPIO as GPIO
import time
import datetime
from hx711_driver import HX711
import json
import os
import asyncio
import websockets
import threading

# LINE SENSOR
LINE_LEFT = 14
LINE_RIGHT = 15
GPIO.setup(LINE_LEFT, GPIO.IN)
GPIO.setup(LINE_RIGHT, GPIO.IN)

# GPIO setup
TRIG = 25
ECHO = 8
BUZZER = 18
DOUT = 5
PD_SCK = 6

RPWM1, LPWM1, R_EN1, L_EN1 = 12, 13, 16, 20
RPWM2, LPWM2, R_EN2, L_EN2 = 22, 19, 21, 26
ENCODER_A, ENCODER_B = 17, 27
ENCODER_C, ENCODER_D = 23, 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(ENCODER_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ENCODER_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ENCODER_C, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ENCODER_D, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup([RPWM1, LPWM1, R_EN1, L_EN1, RPWM2, LPWM2, R_EN2, L_EN2], GPIO.OUT)

pwm_r1 = GPIO.PWM(RPWM1, 1000)
pwm_l1 = GPIO.PWM(LPWM1, 1000)
pwm_r2 = GPIO.PWM(RPWM2, 1000)
pwm_l2 = GPIO.PWM(LPWM2, 1000)

pwm_r1.start(0)
pwm_l1.start(0)
pwm_r2.start(0)
pwm_l2.start(0)

hx = HX711(dout=DOUT, pd_sck=PD_SCK)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(1)
hx.reset()
hx.tare()

wheelRotationCount = 0
routesData = {}
halt_requested = False
reverseMap = {'F': 'B', 'B': 'F', 'L': 'R', 'R': 'L'}

with open("routes.json", 'r') as file:
    routesData = json.load(file)

# Motor control
def move_forward_motor1(speed=50):
    GPIO.output([R_EN1, L_EN1], GPIO.HIGH)
    pwm_r1.ChangeDutyCycle(speed)
    pwm_l1.ChangeDutyCycle(0)

def move_backward_motor1(speed=50):
    print("b")
    GPIO.output([R_EN1, L_EN1], GPIO.HIGH)
    pwm_r1.ChangeDutyCycle(0)
    pwm_l1.ChangeDutyCycle(speed)

def move_forward_motor2(speed=50):
    GPIO.output([R_EN2, L_EN2], GPIO.HIGH)
    pwm_r2.ChangeDutyCycle(speed)
    pwm_l2.ChangeDutyCycle(0)

def move_backward_motor2(speed=50):
    GPIO.output([R_EN2, L_EN2], GPIO.HIGH)
    pwm_r2.ChangeDutyCycle(0)
    pwm_l2.ChangeDutyCycle(speed)

def stop_motor():
    pwm_r1.ChangeDutyCycle(0)
    pwm_l1.ChangeDutyCycle(0)
    pwm_r2.ChangeDutyCycle(0)
    pwm_l2.ChangeDutyCycle(0)

def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.05)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    start_time = time.perf_counter()
    while GPIO.input(ECHO) == 0:
        start_time = time.perf_counter()
    stop_time = time.perf_counter()
    while GPIO.input(ECHO) == 1:
        stop_time = time.perf_counter()
    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2
    return round(distance, 2)


def encoder_callback(channel):
    global wheelRotationCount
    wheelRotationCount += 1

async def execute_command(cmd, websocket=None):
    global halt_requested, wheelRotationCount
    print("IN E C")
    print(f"[LOG] Executing command: {cmd}, HALT status: {halt_requested}")
    if halt_requested:
        print(f"[LOG] HALTED")
        return
    if cmd == 'F':
        print(f"[LOG] Moved FORWARD")
        move_forward_motor1(50)
        move_forward_motor2(50)
    elif cmd == 'B':
        print(f"[LOG] Moved BACK")
        move_backward_motor1(50)
        move_backward_motor2(50)
    elif cmd == 'L':
        print(f"[LOG] Moved LEFT")
        move_backward_motor1(50)
        move_forward_motor2(50)
    elif cmd == 'R':
        print(f"[LOG] Moved RIGHT")
        move_forward_motor1(50)
        move_backward_motor2(50)
    elif cmd == 'S':
        print(f"[LOG] BRAKE")
        stop_motor()
    else:
        print("IN ELSE")
        GPIO.add_event_detect(ENCODER_A, GPIO.RISING, callback=encoder_callback)
        if cmd.startswith("REVERSE"):
            print(f"[LOG] REVERSE: {cmd[7:]} - {routesData[cmd[7:]]}")
            for savedCmd in routesData[cmd[7:]]:
                await execute_command(reverseMap[savedCmd[0]], websocket)
                while wheelRotationCount < savedCmd[1]:
                    # print(f"[LOG] wheelRotationCount: {wheelRotationCount}")
                    time.sleep(0.5)
                wheelRotationCount = 0
        elif cmd.startswith("PROCEED"):
            print(f"[LOG] PROCEED: {cmd[7:]} - {routesData[cmd[7:]]}")
            for savedCmd in routesData[cmd[7:]]:
                await execute_command(savedCmd[0], websocket)
                while wheelRotationCount < savedCmd[1]:
                    # print(f"[LOG] wheelRotationCount: {wheelRotationCount}")
                    time.sleep(0.5)
                wheelRotationCount = 0
        await execute_command("S", websocket)
        if websocket:
            await websocket.send("HALT")
        halt_requested = False
        GPIO.remove_event_detect(ENCODER_A)
        print(f"[LOG] RECORD SERVICE CAME TO AN END")

def end_all():
    stop_motor()
    pwm_r1.stop()
    pwm_l1.stop()
    pwm_r2.stop()
    pwm_l2.stop()
    GPIO.cleanup()

# WebSocket server logic
recvData = "S"
recordingEnabled = False
route = []
command = "S"

# Inside handler (WebSocket server logic)
async def handler(websocket):
    global recvData, halt_requested, recordingEnabled, route, command, wheelRotationCount

    async for message in websocket:
        recvData = message
        print(f"[LOG] Received from frontend: {recvData}")
        
        if recvData == "HALT":
            halt_requested = True
            # await websocket.send("HALT")
            print("[LOG] HALT requested by frontend.")
        
        elif recvData == "FETCH_ROUTES":
            print("[LOG] Sent available routes to frontend.")
            await websocket.send(str(list(routesData.keys())))
        
        elif recvData == "REC_START":
            execute_command("S")
            route = []
            recordingEnabled = True
            GPIO.add_event_detect(ENCODER_A, GPIO.RISING, callback=encoder_callback)
            print("[LOG] Route recording started.")
        
        elif recvData == "LINE":
            await start_line_follow(websocket)

        elif recvData.startswith("REC_STOP"):
            route_name = recvData[8:]
            routesData[route_name] = route
            execute_command("S")
            GPIO.remove_event_detect(ENCODER_A)
            with open("routes.json", 'w') as file:
                json.dump(routesData, file, indent=4)
            route = []
            recordingEnabled = False
            await websocket.send(str(list(routesData.keys())))
            print(f"[LOG] Route recording stopped. Saved as '{route_name}'.")
        
        else:
            if recvData != "S":
                #GPIO.remove_event_detect(ENCODER_A)  # Stop counting
                route.append([recvData, wheelRotationCount])
                print(f"[LOG] Appended to route: [{command}, {wheelRotationCount}]")
                wheelRotationCount = 0
                #GPIO.add_event_detect(ENCODER_A, GPIO.RISING, callback=encoder_callback)
            command = recvData
            print(f"[LOG] Executing command: {command}")
            await execute_command(command, websocket)


# Sensor loop in background
def sensor_loop():
    global command, halt_requested
    sleep_count = 0
    buzzed = False

    while True:
        try:
            if sleep_count == 10:
                distance = get_distance()
                print(f"Distance: {distance:.2f} cm")

                weight = hx.get_weight(5)
                print(f"Weight: {weight:.2f} kg")

                GPIO.output(BUZZER, weight < 35)

                if distance > 500:
                    stop_motor()
                    time.sleep(4)
                    print("distance is less")
                    if get_distance() > 500 and not buzzed:
                        print("distance is less inside if")
                        GPIO.output(BUZZER, False)
                        time.sleep(7)
                        GPIO.output(BUZZER, True)
                        buzzed = True
                else:
                    print("distance isMORE")
                    buzzed = False
                    GPIO.output(BUZZER, True)
                    execute_command(command)

                sleep_count = 0

            time.sleep(0.1)
            sleep_count += 1
        except Exception as e:
            print("Sensor Error:", e)
            break

# Start background thread
threading.Thread(target=sensor_loop, daemon=True).start()

def follow_line():
    left = GPIO.input(LINE_LEFT)
    right = GPIO.input(LINE_RIGHT)

    if left == 0 and right == 0:
        move_forward_motor1(50)
        move_forward_motor2(50)
    elif left == 0 and right == 1:
        move_forward_motor1(20)
        move_forward_motor2(50)
    elif left == 1 and right == 0:
        move_forward_motor1(50)
        move_forward_motor2(20)
    else:
        stop_motor()

async def start_line_follow(websocket):
    global halt_requested
    print("[LOG] Line following started")
    halt_requested = False
    while not halt_requested:
        follow_line()
        await asyncio.sleep(0.1)
    stop_motor()
    await websocket.send("HALT")
    print("[LOG] Line following ended")


# Launch websocket server
async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server running on ws://0.0.0.0:8765")
        await asyncio.Future()  # Run forever

try:
    asyncio.run(main())
except Exception as e:
    end_all()
    print("Error:", e)
finally:
    end_all()