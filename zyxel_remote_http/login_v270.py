import math
from random import random
from time import sleep, time


def performLogin(zyxel, url, username, password):
    login_data = {
        "username": username,
        "password": encode(password),
        "login": 'true',
    }
    # print("Logging in...")
    login_step1 = zyxel.post(url, data=login_data)
    login_check_data = {
        "authId": login_step1.text.strip(),
        "login_chk": 'true',
    }
    # implicitly wait for login to occur
    sleep(1)
    login_step2 = zyxel.post(url, data=login_check_data)
    if 'OK' not in login_step2.text:
        raise Exception("Login failed: %s" % login_step2.text)

def encode(_input):
    # The python representation of the JS function with the same name.
    # This could be improved further, but I can't be bothered.
    password = ""
    possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    _len = lenn = len(_input)
    i = 1
    while i <= (321 - _len):
        if 0 == i % 5 and _len > 0:
            _len -= 1
            password += _input[_len]
        elif i == 123:
            if lenn < 10:
                password += "0"
            else:
                password += str(math.floor(lenn / 10))
        elif i == 289:
            password += str(lenn % 10)
        else:
            password += possible[math.floor(random() * len(possible))]
        i += 1
    return password