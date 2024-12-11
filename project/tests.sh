#!/bin/bash

# Check if Python 3 is installed
if ! command -v python3 >/dev/null 2>&1; then
    echo "Pipeline needs Python 3 but it's not installed."
    exit 1
fi

# Locate requirements.txt dynamically
REQUIREMENTS_FILE="./project/requirements.txt"
if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo "requirements.txt not found in ./project/. Please ensure it exists."
    exit 1
fi

# Install required Python packages
echo "Installing required Python packages..."
python3 -m pip install -r "$REQUIREMENTS_FILE"

# Ensure pytest is installed
if ! python3 -m pytest --version >/dev/null 2>&1; then
    echo "Installing pytest..."
    python3 -m pip install pytest
fi

# Locate pipeline.py dynamically
PIPELINE_FILE="./project/pipeline.py"
if [ ! -f "$PIPELINE_FILE" ]; then
    echo "pipeline.py not found in ./project/. Please ensure it exists."
    exit 1
fi

# Run the ETL pipeline
echo "Running ETL pipeline..."
python3 "$PIPELINE_FILE"

# Check if the ETL pipeline ran successfully
if [ $? -ne 0 ]; then
    echo "ETL pipeline failed. Skipping tests."
    exit 1
fi

# Locate test.py dynamically
TEST_FILE="./project/test.py"
if [ ! -f "$TEST_FILE" ]; then
    echo "test.py not found in ./project/. Please ensure it exists."
    exit 1
fi

# Run the tests
echo "Running test cases..."
pytest "$TEST_FILE"

# Check if tests passed
if [ $? -ne 0 ]; then
    echo "Tests failed."
    exit 1
fi

echo "ETL pipeline and tests executed successfully."

exit 0
