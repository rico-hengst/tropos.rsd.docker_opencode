import os
import random
import time

# import locals
import core_helper

import core_config

# provide timer function
from core_config import timer

# set logger
logger = core_config.setup_logger()

# func
@timer
def rollover_handling():
    x = random.randint(1,3)
    logger.debug("randomized sleep in seconds " + str(x))
    logger.debug("Rollover precedure will be just in time")
    y = time.sleep(x)
    return
    
# func
@timer
def cleanup_desk():
    x = random.randint(0,1)
    logger.debug("Just wait a bit to clean the desk.")
    y = time.sleep(x)
    return
    
    
# main of core module
def main():
    logger.info("Start execution")
    
    # intern functions
    rollover_handling()
    cleanup_desk()
    
    # extern functions
    core_helper.cleansky_check()
    core_helper.landing_maneuver()
    
    logger.info("Stop execution")


if __name__ == "__main__":
    main()
