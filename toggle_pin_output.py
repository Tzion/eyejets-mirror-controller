import time
import RPi.GPIO as GPIO

PIN = 17
FREQUENCY_HZ = 3
WAIT_SEC = 20

def main():
    print("Starting PWN on pin {} with frequency {} Hz".format(PIN, FREQUENCY_HZ))
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.OUT)
    pwm = GPIO.PWM(PIN, FREQUENCY_HZ)
    pwm.start(50.0)
    print(f"Sleeping for {WAIT_SEC} seconds")
    time.sleep(WAIT_SEC)
    pwm.stop()
    GPIO.cleanup()


if __name__ == '__main__':
    main()