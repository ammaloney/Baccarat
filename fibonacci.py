#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Created on Sun Jan 10 10:29:58 2016
@author: amaloney
"""

def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
