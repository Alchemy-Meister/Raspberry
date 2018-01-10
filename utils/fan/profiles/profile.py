#!/usr/bin/env python

from enum import Enum
import configparser

class Profiles(Enum):
    DISABLED = 0
    SILENT = 1
    STANDARD = 2
    TURBO = 3
    USER_DEFINED = 4

class Profile_factory():

    __instance = None

    def __init__(self):
        if self.__instance is not None:
            raise ValueError('An instantiation already exists!')

    def create(self, profile_type):
        if profile_type == Profiles.DISABLED:
            return Disabled()
        elif profile_type == Profiles.SILENT:
            return Silent()
        elif profile_type == Profiles.STANDARD:
            return Standard()
        elif profile_type == Profiles.TURBO:
            return Turbo()
        elif profile_type == Profiles.USER_DEFINED:
            return User_defined()

class Disabled():
    def __init__(self):
        self.enabled = False

class Silent():
    def __init__(self):
        self.enabled = True
        self.max_temp = 70
        self.max_duty = 100
        self.min_temp = 60
        self.min_duty = 72

class Standard():
    def __init__(self):
        self.enabled = True
        self.max_temp = 70
        self.max_duty = 100
        self.min_temp = 45
        self.min_duty = 30

class Turbo():
    def __init__(self):
        self.enabled = True
        self.max_temp = 70
        self.max_duty = 100
        self.min_temp = 0
        self.min_duty = 100

class User_defined():
    __config = configparser.ConfigParser()
    __config.read('config.ini')
    __config = __config['USER_DEFINED_PROFILE']

    def __init__(self):
        self.max_temp = self.to_int_or_float(
            User_defined.__config.get('max_temp', '70')
        )
        self.max_duty = self.to_int_or_float(
            User_defined.__config.get('max_duty', '100')
        )
        self.min_temp = self.to_int_or_float(
            User_defined.__config.get('min_temp', '45')
        )
        self.min_duty = self.to_int_or_float(
            User_defined.__config.get('min_duty', '30')
        )
        if self.min_duty:
            self.enabled = True
        else:
            self.enabled = False
    def to_int_or_float(self, s):
        return float(s) if '.' in s or 'e' in s.lower() else int(s)
