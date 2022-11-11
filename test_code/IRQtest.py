#!/bin/python3
# Author: Nicola Lunghi <nicola.lunghi@emutex.com>
# Modifier: Anson <ansonhe1997@gmail.com>
#   
# Modifed the code to work with new python-periphery API
#
#
# Copyright (c) 2017 Emutex Ltd.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

__version__ = 1.1

from periphery import GPIO
try:
    import queue
except:
    import queue as queue

import threading
import time

# test parameters
PIN_NO = 412 # PIN 13 on ODYSSEY - X86J4105
EDGE_TYPE = "falling"
TIMEOUT = 5


# Wrapper for running poll() in a thread
def threaded_poll(gpio, timeout):
    ret = queue.Queue()

    def f():
        ret.put(gpio.poll(timeout))

    thread = threading.Thread(target=f)
    thread.start()
    return ret, thread


def run(pin_no=PIN_NO, edge_t=EDGE_TYPE, timeout=TIMEOUT):
    threads_list = []

    gpio = GPIO(PIN_NO, "in")
    assert gpio.line == PIN_NO
    assert gpio.fd > 0

    print("GPIO IRQ test on pin %d" % pin_no)
    print("\nPress Ctrl-C to terminate\n")

    try:
        while True:
            gpio.edge = "none"
            print("Check poll falling 1 -> 0 interrupt, current value = ", gpio.read())
            gpio._set_edge = edge_t
            print("Starting thread...")
            poll_ret, _thread = threaded_poll(gpio, timeout)
            threads_list.append(_thread)
            value = poll_ret.get()

            print("Got interrupt! Value = ", value)
            _thread.join()
            print("--------------------")
            print("NEXT CYCLE")

    except KeyboardInterrupt:
        print("\nCtrl-c pressed.\n")

    except:
        print("\nThere was some uncaught error\n")

    finally:
        print("\nTerminating threads...\n")
        while threads_list:
            t = threads_list.pop()
            t.join()
        gpio.edge = "none"
        gpio.direction = "in"
        gpio.close()
        del gpio
        print("\nAll thread terminated exiting.\n")

if __name__ == '__main__':
    run(pin_no=PIN_NO, edge_t=EDGE_TYPE, timeout=TIMEOUT)