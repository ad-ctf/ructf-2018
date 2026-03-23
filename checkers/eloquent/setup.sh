#!/bin/bash
set -euo pipefail

python3 -m pip install --break-system-packages -r requirements.txt
python3 ./install_phantomjs.py
