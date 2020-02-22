#!/usr/bin/env python3
"""
Script to control Vector using external API
This code is based on SDK tutorial #20 asynch_loop_animation
"""
import concurrent
from concurrent import futures
from asyncio import CancelledError
import requests

import anki_vector
from anki_vector import connection
from anki_vector.util import degrees


def stop_motion():
    """
    Stop motion
    """
    robot = anki_vector.Robot()
    robot.connect()
    robot.motors.set_wheel_motors(0, 0, 0, 0)
    robot.disconnect()


def going_out_of_dock():
    """
    Going out of dock
    """
    robot = anki_vector.Robot()
    robot.connect()
    robot.behavior.drive_off_charger()
    robot.disconnect()


def going_on_dock():
    """
    Going on dock
    """
    robot = anki_vector.Robot()
    robot.connect()
    robot.behavior.drive_on_charger()
    robot.disconnect()


def going_left():
    """
    Going left
    """
    robot = anki_vector.Robot()
    robot.connect()
    robot.motors.set_wheel_motors(left_wheel_speed=0,
                                  right_wheel_speed=50,
                                  left_wheel_accel=0,
                                  right_wheel_accel=50)
    robot.disconnect()


def going_right():
    """
    Going right
    """
    robot = anki_vector.Robot()
    robot.connect()
    robot.motors.set_wheel_motors(left_wheel_speed=50,
                                  right_wheel_speed=0,
                                  left_wheel_accel=50,
                                  right_wheel_accel=0)
    robot.disconnect()


def going_front():
    """
    Going front
    """
    robot = anki_vector.Robot()
    robot.connect()
    robot.motors.set_wheel_motors(left_wheel_speed=100,
                                  right_wheel_speed=100,
                                  left_wheel_accel=100,
                                  right_wheel_accel=100)
    robot.disconnect()


def going_back():
    """
    Going back
    """
    robot = anki_vector.Robot()
    robot.connect()
    robot.motors.set_wheel_motors(left_wheel_speed=-100,
                                  right_wheel_speed=-100,
                                  left_wheel_accel=-100,
                                  right_wheel_accel=-100)
    robot.disconnect()


def change_light_color():
    """
    Change light color
    """
    print('Light')
    new_color = input("What color do you want ? "
                      "0(orange) "
                      "1(yellow) "
                      "2(light green) "
                      "3(green) "
                      "4(light blue) "
                      "5(blue) "
                      "6(dark blue) "
                      "7(purple) "
                      "or 8(pink)")
    hue = 0.0
    if new_color == "1":
        hue = 0.1
    if new_color == "2":
        hue = 0.2
    if new_color == "3":
        hue = 0.3
    if new_color == "4":
        hue = 0.4
    if new_color == "5":
        hue = 0.5
    if new_color == "6":
        hue = 0.6
    if new_color == "7":
        hue = 0.7
    if new_color == "8":
        hue = 0.8
    if new_color == "0":
        hue = 0.0
    robot = anki_vector.Robot()
    robot.connect()
    robot.behavior.set_eye_color(hue=hue, saturation=0.76)
    robot.disconnect()


def head_up():
    """
    Head up
    """
    robot = anki_vector.Robot()
    robot.connect()
    robot.behavior.set_head_angle(degrees(15.0))
    robot.disconnect()


def detect_mood():
    """
    Detect mood
    """
    robot = anki_vector.Robot()
    robot.connect()
    robot.vision.enable_display_camera_feed_on_face()
    if robot.conn.requires_behavior_control:
        face_detection = robot.vision.enable_face_detection(detect_faces=robot.enable_face_detection,
                                                            estimate_expression=robot.estimate_facial_expression)
        if isinstance(face_detection, concurrent.futures.Future):
            face_detection.result()
    robot.disconnect()


def head_down():
    """
    Head down
    """
    robot = anki_vector.Robot()
    robot.connect()
    robot.behavior.set_head_angle(degrees(-15.0))
    robot.disconnect()


def lift_up():
    """
    Lift up
    """
    robot = anki_vector.Robot()
    robot.connect()
    robot.behavior.set_lift_height(height=0.9)
    robot.disconnect()


def lift_down():
    """
    Lift down
    """
    robot = anki_vector.Robot()
    robot.connect()
    robot.behavior.set_lift_height(height=0.0)
    robot.disconnect()


def speak(text):
    """
    Speak text
    :param text:
    """
    robot = anki_vector.Robot()
    robot.connect()
    robot.behavior.say_text(text)
    robot.disconnect()


def grab_cube():
    """
    Grab cube
    """
    # If necessary, move Vector's Head and Lift down
    robot = anki_vector.Robot()
    robot.connect()
    robot.behavior.set_head_angle(degrees(-5.0))
    robot.behavior.set_lift_height(0.0)

    print("Connecting to a cube...")
    robot.world.connect_cube()
    robot.behavior.look_around_in_place()
    robot.world.flash_cube_lights()

    if robot.world.connected_light_cube:
        robot.behavior.roll_cube(robot.world.connected_light_cube)
        robot.world.disconnect_cube()

    robot.disconnect()


async def playing(action):
    """
    Launch action
    :param action:
    """
    action = action.text.lower().replace('\r', '').replace('\n', '').replace('"', '')

    if action:
        print(f"Action {action}")

    status = True

    if 'stop_motion' == action:
        # Stop motion
        print("Stop")
        stop_motion()

    elif action in ('off_charger', 'out'):
        # Going out of charger
        print("Out of charger")
        going_out_of_dock()

    elif action in ('on_charger', 'going in'):
        # Going on charger
        print("Going on charger")
        going_on_dock()

    elif action in ('left', 'gauche'):
        # Going left
        print('Going left')
        going_left()

    elif action in ('right', 'droite'):
        # Going right
        print('Going right')
        # robot.behavior.turn_in_place(degrees(-30))
        going_right()

    elif action in ('up_dir', 'front', 'avancer', 'devant', 'avant'):
        # Going front
        print('Going front')
        going_front()

    elif action in ('down_dir', 'reculer', 'back'):
        # Going back
        print('Going back')
        going_back()

    elif action == 'light':
        # Change light
        print('Change light')
        change_light_color()

    elif action == 'head_up':
        # Head up
        print('Head up')
        head_up()

    elif action == 'head_down':
        # Head down
        print('head_down')
        head_down()

    elif action == 'lift_up':
        # Lift up
        print('lift_up')
        lift_up()

    elif action == 'lift_down':
        # Lift down
        print('lift_down')
        lift_down()

    elif action == 'mood':
        # Detect move
        print('Vector is watching...')
        detect_mood()

    elif 'say' in action:
        # Pronounce the input text
        print('Hum hum...(ready to speak aloud)')
        speak(action.replace('say', ''))

    elif action == 'grab':
        # Grab the cube
        print('I will grab the cube')
        grab_cube()

    elif action in ('quit', 'exit', 'close'):

        # Quit
        status = False

    return status


async def play():
    """
    Main method to play with anki-vector
    """
    run = True
    while run:
        try:
            
            # Yes that's a big up for Heroku !!
            url = "https://<API>.herokuapp.com/read"
            
            run = await playing(requests.get(url))
        except CancelledError:
            raise  # aiohttp will cope with error

    return run


if __name__ == "__main__":
    conn = anki_vector.connection.Connection("Vector-S3K9", "<IP USED IN VECTOR SDK TUTORIAL #20>:443",
                                             'Vector-<ID>.cert',
                                             "<SECRET>")
    conn.connect()
    conn.run_coroutine(play()).result()
    conn.close()
