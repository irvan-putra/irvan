#!/usr/bin/env bash
cd "$(dirname "$0")/.." 
set -euo pipefail
adb install -r app/build/outputs/apk/debug/irvan-v*-debug.apk
python3 ci/smoke.py
