import time
import RPi.GPIO as GPIO

PIN = 17
FREQUENCY_HZ = .5
WAIT_SEC = 10

def main():
    print(f"Starting step function on pin {PIN} with frequency {FREQUENCY_HZ} Hz")
    period = 1.0 / FREQUENCY_HZ  # Calculate the period
    high_time = period / 2  # High for half the period
    low_time = period / 2  # Low for half the period

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.OUT)

    start_time = time.time()
    while (time.time() - start_time) < WAIT_SEC:
        GPIO.output(PIN, GPIO.HIGH)  # Set pin high
        time.sleep(high_time)  # Wait for high_time
        GPIO.output(PIN, GPIO.LOW)  # Set pin low
        time.sleep(low_time)  # Wait for low_time

    GPIO.cleanup()


if __name__ == '__main__':
    main()