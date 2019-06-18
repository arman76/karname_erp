# -*- coding: utf-8 -*-
import _thread
from time import sleep
import scrp

ml = []


def main(bot):
    _thread.start_new_thread(update_list, (5,))
    while True:
        for user in ml:
            scrp.main(bot, user.split('=')[0], {'username' : (user.split('=')[1]).split(':')[0], 'password' : (user.split('=')[1]).split(':')[1]})
            sleep(5)


def update_list(t):
    while True:
        with open('list.txt', 'r') as f:
            for l in f.readlines():
                ml.append(l.replace('\n', ''))
        sleep(t)
