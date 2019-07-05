#!/usr/bin/env python3
import os
import sys
import time
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, SpeedPercent, MoveTank, MoveSteering, MediumMotor, OUTPUT_B
from ev3dev2.sensor import INPUT_1, INPUT_4, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import TouchSensor, InfraredSensor, ColorSensor
from ev3dev2.led import Leds
from ev3dev2.button import Button
from ev3dev2.sound import Sound
ON = True
OFF = False

music = Sound()
music.play_file("Confirm.wav")
tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
steering_drive = MoveSteering(OUTPUT_A, OUTPUT_D)
ir = InfraredSensor()
ir.mode = "IR-PROX"
touch_sensor = TouchSensor()
touch_sensor.mode = "TOUCH"
color_arm = MediumMotor(OUTPUT_B)
display_button = Button()
color_sensor = ColorSensor()

def deploy_color_sensor():
    color_arm.on_for_rotations(SpeedPercent(5), 0.30)
    time.sleep(4.5)
    if color_sensor.color == 1:
        music.speak("I found something black on the surface of Mars")
    elif color_sensor.color == 2:
        music.speak("I found water on the surface of Mars")
    elif color_sensor.color == 3:
        music.speak("I found a plant on the surface of Mars")
    elif color_sensor.color == 4:
        music.speak("I found something yellow on the surface of Mars")
    elif color_sensor.color == 5:
        music.speak("I found a rock on the surface of Mars")
    elif color_sensor.color == 6:
        music.speak("I found something white on the surface of Mars")
    elif color_sensor.color == 7:
        music.speak("I found a rock on the surface of Mars")
    color_arm.on_for_rotations(SpeedPercent(-15), 0.3)
    time.sleep(3)

demo_count = 0

while True:
    tank_drive.on(SpeedPercent(50), SpeedPercent(50))

    if ir.value() > 70:
        tank_drive.on_for_seconds(SpeedPercent(-50), SpeedPercent(-50), 1)
        steering_drive.on_for_seconds(90, SpeedPercent(75), 1)
        demo_count += 1

    elif ir.value() < 35:
        tank_drive.off()
        music.play_file("Overpower.wav")
        deploy_color_sensor()
        demo_count += 1

    elif touch_sensor.is_pressed:
        tank_drive.off()
        music.play_note("F4", 0.5)
        music.play_note("D4", 0.5)
        deploy_color_sensor()
        demo_count += 1

    elif demo_count == 10:
        tank_drive.off()
        music.play_file("Download.wav")
        music.play_file("Download.wav")
        music.speak("I have gathered all the necessary data. Now I will send this all back to Earth")
        music.speak("Thank you for watching this demo")
