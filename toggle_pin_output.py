import time
import RPi.GPIO as GPIO

PINS = [17, 27]
FREQUENCY_HZ = .05
DURATION_SEC = 22

def main():
    print(f"Starting step function on pin {PINS} with frequency {FREQUENCY_HZ} Hz")
    period = 1.0 / FREQUENCY_HZ  # Calculate the period
    high_time = period / 2  # High for half the period
    low_time = period / 2  # Low for half the period

    GPIO.setmode(GPIO.BCM)
    for pin in PINS:
        GPIO.setup(pin, GPIO.OUT)

    start_time = time.time()
    print("Starting cycle")
    while (time.time() - start_time) < DURATION_SEC:
        for pin in PINS:
            GPIO.output(pin, GPIO.HIGH)  # Set pin high
        time.sleep(high_time)  # Wait for high_time
        for pin in PINS:
            GPIO.output(pin, GPIO.LOW)  # Set pin low
        time.sleep(low_time)  # Wait for low_time

    for pin in PINS:
        GPIO.cleanup(pin)


if __name__ == '__main__':
    main()