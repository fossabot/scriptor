"""
Scriptor is a open-source CLI tool designed for simple management of your local and cloud environments tailored to your home-labs or business environments
"""

import sys
from importlib.metadata import version
from loguru import logger

__VERSION__ = version("scriptor")

logger.remove()
logger.add(sys.stderr, level="WARNING")
logger.add("scriptor.log", rotation="50 MB", level="DEBUG")
