#!/usr/bin/env python
import time
import math
import zmq
import random
import numpy as np
import matplotlib.pyplot as plt

class InstrumentPrice(object):
    def __init__(self) -> None:
        self.symbol = "SYMBOL"
        self.t = time.time()
        self.value = 100.0
        self.sigma = 0.4
        self.r = 0.01

    def simulate_value(self) -> float:
        """
        Generates a new, random stock price.
        """
        t = time.time()
        dt = (t - self.t) / (252 * 8 * 60 * 60)
        dt *= 500
        self.t = t
        self.value *= math.exp(
            (self.r - 0.5 * self.sigma**2) * dt
            + self.sigma * math.sqrt(dt) * np.random.normal(0, 1)
        )
        return self.value

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://0.0.0.0:5555')

ip = InstrumentPrice()

while True:
    msg = '{} {:.2f}'.format(ip.symbol, ip.simulate_value())
    print(msg)
    socket.send_string(msg)
    time.sleep(random.random() * 2)
