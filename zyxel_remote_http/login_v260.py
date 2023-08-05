import math
import requests
from random import random
from time import sleep, time

def performLogin(zyxel, url, username, password):
    login_data = {
        "login": 1,
        "username": username,
        "password": encode(password),
        "dummy": current_time()
    }
    login_check_data = {
        "login_chk": 1,
        "dummy": current_time()
    }

    # print("Logging in...")
    zyxel.get(url, params=login_data)
    # implicitly wait for login to occur
    sleep(1)
    ret2 = zyxel.get(url, params=login_check_data)
    # 'OK' if logged in
    # 'AUTHING' if not logged in
    if 'OK' not in ret2.http_response.text:
        raise Exception("Login failed: %s" % ret2.text)

    # print("Login successful, parsing cookie.")
    cookie = parse_cookie(zyxel.get(url, params={"cmd": 2}).http_response)
    # print("Got COOKIE: %s" % cookie)
    zyxel.session.cookies.set("XSSID", cookie)

def encode(_input):
    # The python representation of the JS function with the same name.
    # This could be improved further, but I can't be bothered.
    password = ""
    possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    _len = lenn = len(_input)
    i = 1
    while i <= (320 - _len):
        if 0 == i % 7 and _len > 0:
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

def current_time():
    return int(time() * 1000.0)

def parse_cookie(cmd_1: requests.Response):
    for line in cmd_1.text.split("\n"):
        if 'XSSID' in line:
            return line.replace('setCookie("XSSID", "', '').replace('");', '').strip()
