# -*- coding: utf-8 -*-

from rules.rule import *

class Rule(KLCRule):
    """
    Create the methods check and fix to use with the kicad lib files.
    """
    def __init__(self, component):
        super(Rule, self).__init__(component, 'Pin requirements')

    def checkPinOrigin(self):
        self.violating_pins = []
        err = False
        for pin in self.component.pins:
            posx = int(pin['posx'])
            posy = int(pin['posy'])
            if (posx % 100) != 0 or (posy % 100) != 0:
                self.violating_pins.append(pin)
                if not err:
                    self.error("Pins not located on 100mil grid:")
                self.error(' - Pin {0} ({1}), {2}'.format(pin['name'], pin['num'], positionFormater(pin)))
                err = True

        return len(self.violating_pins) > 0

    def checkDuplicatePins(self):
        # List of lists of pins
        pin_lists = []

        # look for duplicate pin numbers
        # For a pin to be considered a duplicate, it must have:
        # - The same number
        # - Be in the same unit
        # - Be in the same "convert"

        keys = ['num', 'unit', 'convert']

        for pin in self.component.pins:

            found = False

            for i,pin_list in enumerate(pin_lists):

                # Compare against first item
                p_test = pin_list[0]

                # Test each key
                if all([pin[k] == p_test[k] for k in keys]):
                    found = True
                    pin_lists[i].append(pin)
                    break

            if not found:
                pin_lists.append([pin])

        duplicate = False

        for pin_list in pin_lists:
            # Look for duplicate groups
            if len(pin_list) > 1:
                duplicate = True
                self.error("Pin {n} is duplicated:".format(n=pin_list[0]['num']))

                for pin in pin_list:
                    self.errorExtra(pinString(pin))

        return duplicate

    def checkPinLength(self):
        self.violating_pins = []

        for pin in self.component.pins:
            length = int(pin['length'])

            err = False

            # ignore zero-length pins e.g. hidden power pins
            if length == 0: continue

            if length < 50:
                self.error("{pin} length ({len}mils) is below 50mils".format(pin=pinString(pin), len=length))
            elif length < 100:
                self.warning("{pin} length ({len}mils) is below 100mils".format(pin=pinString(pin), len=length))


            if length % 50 != 0:
                self.warning("{pin} length ({len}mils) is not a multiple of 50mils".format(pin=pinString(pin), len=length))

            # length too long flags a warning
            if length > 300:
                err = True
                self.error("{pin} length ({length}mils) is longer than maximum (300mils)".format(
                    pin = pinString(pin),
                    length = length))

            if err:
                self.violating_pins.append(pin)

        return len(self.violating_pins) > 0

    def check(self):

        return any([
            self.checkPinOrigin(),
            self.checkPinLength(),
            self.checkDuplicatePins()
            ])


        return True if len(self.violating_pins) > 0 else False

    def fix(self):
        """
        Proceeds the fixing of the rule, if possible.
        """

        self.info("Fix not supported")

        if self.checkPinOrigin():
            pass

        if self.checkPinLength():
            pass