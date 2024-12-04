#!/bin/bash

# Check if Python 3 is installed
if ! command -v python3 >/dev/null 2>&1; then
    echo "Pipeline needs Python 3 but it's not installed."
    exit 1
fi

# Install required Python packages
echo "Installing required Python packages..."
python3 -m pip install -r ./requirements.txt

# Ensure pytest is installed
if ! python3 -m pytest --version >/dev/null 2>&1; then
    echo "Installing pytest..."
    python3 -m pip install pytest
fi

# Run the data pipeline
echo "Running data pipeline..."
python3 ./pipeline.py

# Check if the data pipeline ran successfully
if [ $? -ne 0 ]; then
    echo "Data pipeline failed. Skipping tests."
    exit 1
fi

# Run the tests
echo "Running test cases..."
pytest ./tests/test_pipeline.py

# Check if tests passed
if [ $? -ne 0 ]; then
    echo "Tests failed."
    exit 1
fi

echo "Tests passed successfully."

exit 0
