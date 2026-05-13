"""Run AETHER OS"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import asyncio
from aether_os.main import demo_workflow

if __name__ == "__main__":
    asyncio.run(demo_workflow())
