#!/usr/bin/env python
from xinput import *
from os.path import isfile
import pyglet
import time
import playsound
import threading

controls_disabled = False
menu_opened = True

timer_start = time.perf_counter()
timer_last_tp = time.perf_counter()
timer_last_update = time.perf_counter()
pause_time = 0

if __name__ == '__main__':
    timer_start = time.perf_counter()
    timer_last_update = time.perf_counter()

    # Initialize the controller
    joysticks = XInputJoystick.enumerate_devices()
    device_numbers = list(map(attrgetter('device_number'), joysticks))

    print(f'Found {len(joysticks)} devices: {device_numbers}')

    if not joysticks:
        print('No xinput controllers found :(')
        input('Press ENTER to exit...')
        sys.exit(0)

    j = joysticks[0]
    print(f'Using first controller with id {joysticks[0]}')

    battery = j.get_battery_information()
    print(f'Controller type: {battery[0]}, battery status: {battery[1]}')

    # Read the start, confirm and options button
    if not isfile('./settings.txt'):
        with open('./settings.txt', 'w') as f:
            f.write('menu=\n')
            f.write('confirm=\n')
            f.write('resync=\n')
            f.write('disable=\n')
            f.write('seconds_before=2\n')
            f.write('sound_file=./notification.wav\n')

        print('In the script working directory a "settings.txt" file was created.')
        print('You can now use the controller to identify the IDs for:')
        print(' * menu button\t(opening menu, most likely "Options"),')
        print(' * confirm button\t(used for closing menu), most likely "A"')
        print(' * resync button\t(to reset the timer with), "recommended "L3"')
        print(' * disable button\t(to temporary disable the script so you can navigate the menu without timer starting early), recommended "R3",')
        print('then input the ids right after the "=" in the settings file without spaces.')
        print('In the settings you can also set how many seconds before the teleport you want to be notified, and what file to play.')

        @j.event
        def on_button(button, pressed):
            print('Button ID:', button, 'Pressed' if pressed == 1 else 'Released')

        @j.event
        def on_axis(axis, value):
            pass

        while True:
            j.dispatch_events()
            time.sleep(.01)

    else:
        with open('./settings.txt', 'r') as f:
            lines = [ line.split(sep='=') for line in f.readlines() ]
            options = { line[0]: line[1].strip() for line in lines }

        @j.event
        def on_button(button, pressed):
            global controls_disabled, menu_opened, timer_last_tp, timer_start, timer_last_update, pause_time
            
            if pressed != 0:
                return
        
            if not controls_disabled:

                if button == int(options['menu']):
                    if not menu_opened:
                        menu_opened = True
                        pause_time = time.perf_counter()
                        print('Pressed MENU : Stopping timer')

                if button == int(options['confirm']):
                    if menu_opened:
                        menu_opened = False
                        timer_now = time.perf_counter()
                        timer_start += timer_now - pause_time
                        timer_last_update += timer_now - pause_time
                        timer_last_tp += timer_now - pause_time
                        print('Pressed CONFIRM : Starting timer')

                if button == int(options['resync']):
                    timer_start = time.perf_counter()
                    print('Pressed RESYNC : Started timer from 0')

            if button == int(options['disable']):
                if not controls_disabled:
                    controls_disabled = True
                    print('Pressed DISABLE : Disabled controls until another DISABLE pressed')
                else:
                    controls_disabled = False
                    print('Pressed DISABLE : Enabled controls back again')

        TP_SECS = 22

        while True:
            if not menu_opened:
                timer_now = time.perf_counter()
                
                if timer_start > timer_last_tp:
                    timer_last_tp = timer_start
                    timer_last_update = timer_now

                if timer_now - timer_last_update > 0.005:
                    # Called every second
                    timer_last_update = timer_now
                    if (timer_now - timer_last_tp) % 1 < 0.012:

                        sec_from_last_tp = int(timer_now - timer_last_tp)
                        sec_to_next_tp = TP_SECS - sec_from_last_tp
                        info_string = f'Seconds before next TP: {sec_to_next_tp} ----===#'

                        if sec_to_next_tp == int(options['seconds_before']):
                            threading.Thread(target=lambda: playsound.playsound(options['sound_file'])).start()


                        if timer_now - timer_last_tp >= TP_SECS:
                            info_string += ' TELEPORTING'
                            timer_last_tp = timer_now
                        
                        print(info_string)

            j.dispatch_events()
            time.sleep(.01)