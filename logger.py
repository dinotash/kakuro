"""
Convenience module to initalize logging output in a common format for use
in various related scripts.
"""

import sys
import logging

def setup_logger():
    """
    Initializes logging to print INFO level messages to std out.
    Should be called from main() at start of script.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    steam_handler = logging.StreamHandler(sys.stdout)
    steam_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    steam_handler.setFormatter(formatter)
    logger.addHandler(steam_handler)
