#!/bin/bash

# Wrapper script to run the email monitor with the correct environment for cron.

# --- IMPORTANT ---
# 1. This script MUST be run from the DIV-5 directory.
# 2. Replace the placeholder values below with your actual credentials.
#    Use the APP-SPECIFIC PASSWORD you generated, NOT your main email password.

# Set the full path to your project directory
PROJECT_DIR="/Users/homebase/Desktop/1R-MASTER/DIV-5"

# Export the environment variables the Python script needs
export IMAP_SERVER="imap.mail.me.com" # Or imap.gmail.com, etc.
export EMAIL_USER="your_email@icloud.com"
export EMAIL_PASS="xxxx-xxxx-xxxx-xxxx" # Your app-specific password

# Navigate to the project directory
cd "$PROJECT_DIR" || exit

# Activate the Python virtual environment and run the script
# We use the full path to the python executable inside the venv
./.venv/bin/python ./scripts/monitor_email.py