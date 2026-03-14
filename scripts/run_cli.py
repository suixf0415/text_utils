#!/usr/bin/env python3
"""CLI entry point wrapper."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from text_utils.cli import main

if __name__ == "__main__":
    sys.exit(main())
