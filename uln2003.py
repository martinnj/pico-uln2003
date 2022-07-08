"""
Module containing code to run a stepper motor via the ULN2003 driver board.

Basically a refactor from https://github.com/IDWizard/uln2003/
"""

from machine import Pin
import utime

__HALF_STEP_TABLE = [
    [0, 0, 0, 1],
    [0, 0, 1, 1],
    [0, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 0],
    [1, 1, 0, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 1],
]

__FULL_STEP_TABLE = [
 [1, 0, 1, 0],
 [0, 1, 1, 0],
 [0, 1, 0, 1],
 [1, 0, 0, 1]
]

class ULN2003(object):
    """
    Class representing an ULN2003 stepper driver.
    The default settings are made to work with the 28byj-48 5V DC stepper motor.
    """

    pins = list()
    steps_pr_rotation = 0
    step_table = list()
    interval = 0

    def __init__(self, pins: list[int], half_step: bool=True, interval: float=0.001, steps_pr_rotation: int=None):
        """
        ### Arguments
        - pins : list[int]
          A list of integers representing the IO pins used to control the stepper motor.
        - half_step : bool (Default: True)
          Should movements be in half-steps or whole-steps.
        - interval : float (Default: 0.001)
          Number of seconds to sleep between each sub-step. Smaller values give faster movement.
          If this becomes too low, the motor might just stop moving.
        - full_rotation : int (Default: None)
          How many steps are in a full rotation. If set to None, a default based on the 28byj-48.
        """

        # Create GPIO pin objects.
        self.pins = [Pin(p, Pin.OUT, 0) for p in pins]

        # Set the correct step table.
        self.step_table = __HALF_STEP_TABLE if half_step else __FULL_STEP_TABLE

        # Set how many steps in a rotation.
        # From http://www.jangeox.be/2013/10/stepper-motor-28byj-48_25.html
        self.steps_pr_rotation = steps_pr_rotation if steps_pr_rotation else int(4075.7728395061727/8)

        # Set interval between steps.
        self.interval = interval


    def __reset(self):
        """ Set all output pins to 0. """
        for pin in self.pins:
            pin.value(0)

    def move(self, steps: int=1, direction: int=1):
        """
        Move the stepper motor a specific number of steps in one direction.

        ### Arguments
        - steps : int (Default: 1)
          How many steps to move in the specified direction.
        - direction : int (Default: 1)
          The direction to move. Must be either: 1 for forward, or -1 for backwards.
        """
        for _ in range(steps):
            for state in self.step_table[::direction]:
                for p in range(4):
                    self.pins[p].value(state[p])
                utime.sleep(self.interval)
        self.__reset()

    def rotate_once(self, direction: int=1):
        """
        Move a full rotation in the specified direction.

        ### Arguments
        - direction : int (Default: 1)
          The direction to move. Must be either: 1 for forward, or -1 for backwards.
        """
        self.move(self.steps_pr_rotation, direction)

