# Pico ULN2003

Micropython Module containing code to run a stepper motor via the ULN2003 driver
board from a Raspberry Pi Pico.

Baiscally a refactor from https://github.com/IDWizard/uln2003/

## Usage

Hook up 4 pins from the Pi Pico to the pins on the ULN2003, in my example I used
GPIO 0-3, and remember to connect 5V power to driver board.

```python
from uln2003 import ULN2003

stepper = ULN2003([0,1,2,3])

# Rotate fully in both directions.
stepper.rotate_once(1)
stepper.rotate_once(-1)

# Take small steps forever.
while True:
    print("A small step for man!")
    stepper.move(1)
```
