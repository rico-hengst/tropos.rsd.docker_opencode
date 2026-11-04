import os
import random
import time

# import locals
import core_config

# provide timer function
from core_config import timer

# set logger
logger = core_config.setup_logger()

# helper func
@timer
def cleansky_check():
    x = random.randint(1,3)
    y = time.sleep(x)
    logger.warning("That's not what transparency looks like")
    return
    
# helper func
@timer
def landing_maneuver():
    x = random.randint(2,4)
    logger.debug("Soft touch down expected!")
    y = time.sleep(x)
    return
    
    

