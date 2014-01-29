from src.logical_core import *
from src.driver_first_try import Driver

new_driver = driver_first_try.Driver()
for action in new_driver.actuator.actions:
	action.execute()