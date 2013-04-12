#!/usr/bin/env python
# vim: fileencoding=utf-8: expandtab: softtabstop=4: shiftwidth=4: foldmethod=marker: fmr=#{,#}

"""
TrollBox v0.1

btc-e.com chat channal
"""

from   __future__ import print_function
import websocket
from   json       import loads as jsload

COLOR_0   = "\033[m"      # серый
COLOR_1   = "\033[1m"     # жирный (bold)
COLOR_2   = "\033[0;32m"  # зелёный
COLOR_3   = "\033[1;32m"  # ярко-зелёный
COLOR_4   = "\033[0;33m"  # жёлтый
COLOR_5   = "\033[1;33m"  # ярко-жёлтый
COLOR_6   = "\033[0;36m"  # бирюзовый
COLOR_7   = "\033[1;36m"  # ярко-бирюзовый
COLOR_8   = "\033[1;31m"  # ярко-красный
COLOR_9   = "\033[1;34m"  # серый
COLOR_10  = "\033[1;30m"  # ярко-синий

COLORS   = (COLOR_2, COLOR_3,
            COLOR_4, COLOR_5, COLOR_6, COLOR_7,
            COLOR_8, COLOR_9)

CHAT_URL = "wss://ws.pusherapp.com/app/4e0ebd7a8b66fa3554a4?protocol=6&client=js&version=2.0.0&flash=false"

def get_chat_connection():
    ws = websocket.WebSocket()
    ws.connect(CHAT_URL)
    return ws

def chat_handshake(ws):
    hello_msg = """{"event":"pusher:subscribe","data":{"channel":"chat_ru"}}"""
    server_hello = ws.recv()
    ws.send(hello_msg)

    subscribe_status = ws.recv()
    return jsload(subscribe_status)

def deserialize(json):
    obj_lvl1 = jsload(json)
    return jsload(jsload(obj_lvl1.get("data", "{}")))

def main():
    print("BTC-E TrollBOX")
    print("Connecting...", end = " ")

    ws = get_chat_connection()
    chat_handshake(ws)
    print("OK\n\n")

    while True:
        chat_message = ws.recv()
        struct = deserialize(chat_message)

        login = struct.get("login", "")

        format_params = {
            "login"     : login,
            "date"      : struct.get("date",  ""),
            "msg"       : struct.get("msg",   "").encode("utf-8"),
            "login_clr" : COLORS[hash(login) % len(COLORS)],
            "colon_clr" : COLOR_10,
            "nocollor"  : COLOR_0
        }

        print("{login_clr}{login:13}{colon_clr}: {nocollor} {msg} ".format(**format_params))

if __name__ == "__main__":
    main()
