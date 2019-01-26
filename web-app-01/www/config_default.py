#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Default configurations.
'''

__author__ = 'Michael Liao'

configs = {
    'debug': True,
    'db': {
        'host': '192.168.1.111',
        'port': 3306,
        'user': 'dev',
        'password': 'dev',
        'db': 'zun_qy_pay'
    },
    'session': {
        'secret': 'Awesome'
    }
}