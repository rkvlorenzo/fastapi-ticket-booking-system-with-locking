#!/bin/bash

# Enable automatic export of variables
set -o allexport

# Source the .env file. Adjust the path if your .env file is not in the same directory.
source ./.env

uvicorn app.main:app --reload
