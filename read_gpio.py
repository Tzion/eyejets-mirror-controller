import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
gpio_pin = 17
GPIO.setup(gpio_pin, GPIO.IN)
input_value = GPIO.input(gpio_pin)

while True:
    try:
        print("Input value:", input_value)
    except KeyboardInterrupt:
        GPIO.cleanup()