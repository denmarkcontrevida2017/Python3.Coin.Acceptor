# Copyright (c) CMNWorks
# Licensed under The MIT License
#
# @copyright     Copyright (c) CMNWorks Christopher M. Natan
# @author        Christopher M. Natan
# @link          http://cmnworks.com
# @license       http://www.opensource.org/licenses/mit-license.php MIT License


import RPi.GPIO as GPIO
import threading
import sys

GPIO_PIN = 15
TIME_OUT = 150000


class CoinAcceptor:
    coin_inserted = 0

    def __init__(self):
        pass

    def listen(self):
        GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        print("Listening to incoming pulse")
        GPIO.add_event_detect(GPIO_PIN, GPIO.RISING)

        reset_counter = 0
        while True:
            if GPIO.event_detected(GPIO_PIN):
                reset_counter = 1
                self.coin_inserted += 1
                inserted = str(self.coin_inserted)
                print('Pulse detected and the value is: ' + inserted)
            if reset_counter >= 1:
                reset_counter += 1
            if reset_counter >= TIME_OUT:
                print('The total pulse accepted: ' + str(self.coin_inserted))
                self.coin_inserted = 0
                reset_counter = 0


try:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    coin_acceptor = CoinAcceptor()

    coinAcceptorThread = threading.Thread(name='CoinAcceptor', target=coin_acceptor.listen())
    coinAcceptorThread.start()
    coinAcceptorThread.join()

except (KeyboardInterrupt, SystemExit):
    print("Keyboard interrupt")
finally:
    print("Finish")
    GPIO.cleanup()
