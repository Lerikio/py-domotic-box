from src.logical_core import *
from src.driver_first_try import Driver

new_driver = Driver()
for action in new_driver.actuator.actions:
	action.execute()