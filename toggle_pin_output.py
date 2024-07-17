import time
import RPi.GPIO as GPIO
import argparse

PINS = [17, 27]
FREQUENCY_HZ = .2  # in high frequencies add 2% to the desired freq to compensate the pi delay
DURATION_SEC = 20


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--freq', type=float, help='Frequency (Hertz) of the pulse function', default=1)
    parser.add_argument('--duration', type=float, help='Duration in seconds', default=DURATION_SEC)
    # parser.add_argument('')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    print(f"Starting step function on pin {PINS} with frequency {args.freq} Hz")
    period = 1.0 / args.freq  # Calculate the period
    high_time = period / 2  # High for half the period
    low_time = period / 2  # Low for half the period

    GPIO.setmode(GPIO.BCM)
    for pin in PINS:
        GPIO.setup(pin, GPIO.OUT)

    start_time = time.time()
    print("Starting cycle")
    while (time.time() - start_time) < args.duration:
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