#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

if [ -f ".venv/Scripts/activate" ]; then
    source ".venv/Scripts/activate"
    PYTHON_BIN=".venv/Scripts/python.exe"
elif [ -f ".venv/bin/activate" ]; then
    source ".venv/bin/activate"
    PYTHON_BIN=".venv/bin/python"
else
    echo "Virtual environment not found" >&2
    exit 1
fi

"$PYTHON_BIN" -m pytest