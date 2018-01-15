#!/usr/bin/env python

import configparser
import RPi.GPIO as gpio
import time
import signal
from profiles import Profiles, Profile_factory

# Returns CPU temperature value as float
def get_cpu_temperature():
    with open('/sys/devices/virtual/thermal/thermal_zone0/temp', 'r') \
        as file:
        
        str_temp = file.readline()
        print(str_temp)
        return float(str_temp) / 1000

def calculate_linear_function_variables(y1, y2, x1, x2):
    b = (y2 - y1) / (-x1 + x2)
    a = -x1 * ((y2 -y1) / (-x1 + x2)) + y1

    return a, b

def calculate_fan_duty(a, b, current_cpu_temp, profile_min_temp):
    if current_cpu_temp >= profile_min_temp:
        return a + b * current_cpu_temp
    else:
        return 0

def on_exit_signal(signum, frame):
    raise Exception('exit signal received')

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config = config['FAN_CONFIG']

    fan_pin = int(config.get('fan_pin', 12))
    fan_frequency = int(config.get('fan_frequency', 50))
    print(fan_frequency)
    update_interval = int(config.get('update_interval', 15))
    str_fan_profile = config.get('str_fan_profile', 'STANDARD')
    
    fan_profile = Profile_factory().create(Profiles[str_fan_profile])
    if fan_profile.enabled:
        a, b = calculate_linear_function_variables(fan_profile.min_duty, \
            fan_profile.max_duty, fan_profile.min_temp, fan_profile.max_temp)

    gpio.setmode(gpio.BOARD)
    gpio.setup(fan_pin, gpio.OUT)
    fan_pwd = gpio.PWM(fan_pin, fan_frequency)
    
    signal.signal(signal.SIGINT, on_exit_signal)
    signal.signal(signal.SIGTERM, on_exit_signal)

    while(fan_profile.enabled):
        try:
            cpu_temp = get_cpu_temperature()
            fan_power = calculate_fan_duty(a, b, cpu_temp, fan_profile.min_temp)
            print(fan_power)
            if fan_power != 0:
                 fan_pwd.start(fan_power)
            else:
                 fan_pwd.stop()
            
            time.sleep(update_interval)
        except Exception:
            gpio.cleanup()
            break

if __name__ == '__main__':
    main()
