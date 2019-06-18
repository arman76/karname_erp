# -*- coding: utf-8 -*-
from time import sleep
import scrp

ml = []


def main(bot):
    while True:
        for user in ml:
            scrp.main(bot, user.split('=')[0], {'username' : (user.split('=')[1]).split(':')[0], 'password' : (user.split('=')[1]).split(':')[1]})
            sleep(5)
        with open('list.txt', 'r') as f:
            for l in f.readlines():
                ml.append(l.replace('\n', ''))

