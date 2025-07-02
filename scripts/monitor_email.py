#!/usr/bin/env python3
"""
Email Monitor Script for DIV-5 Project

This script connects to an IMAP email server, monitors for new emails from specific addresses,
and automatically downloads them to the appropriate directory for processing.
It's designed to be run periodically via cron using the run_email_monitor.sh wrapper.
"""

import os
import sys
import imaplib
import email
from email import policy
from email.parser import BytesParser
import time
from datetime import datetime
import re
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/email_monitor.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Configuration - read from environment variables
IMAP_SERVER = os.environ.get('IMAP_SERVER')
EMAIL_USER = os.environ.get('EMAIL_USER')
EMAIL_PASS = os.environ.get('EMAIL_PASS')
ALLOWED_SENDERS = os.environ.get('ALLOWED_SENDERS', '').split(',')

# Directory where emails will be saved
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL_STORAGE_DIR = os.path.join(BASE_DIR, "incoming_emails")
PROCESSED_DIR = os.path.join(BASE_DIR, "_extracted_text")

# Create directories if they don't exist
os.makedirs(EMAIL_STORAGE_DIR, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "logs"), exist_ok=True)

# Track processed emails
PROCESSED_IDS_FILE = os.path.join(BASE_DIR, "logs", "processed_email_ids.txt")

def load_processed_ids():
    """Load IDs of emails that have already been processed."""
    if not os.path.exists(PROCESSED_IDS_FILE):
        return set()
    
    with open(PROCESSED_IDS_FILE, 'r') as f:
        return set(line.strip() for line in f)

def save_processed_id(email_id):
    """Save an email ID as processed."""
    with open(PROCESSED_IDS_FILE, 'a') as f:
        f.write(f"{email_id}\n")

def sanitize_filename(filename):
    """Convert a string to a valid filename."""
    # Replace invalid characters with underscores
    filename = re.sub(r'[\\/*?:"<>|]', '_', filename)
    # Limit length to avoid excessively long filenames
    if len(filename) > 100:
        filename = filename[:97] + "..."
    return filename

def connect_to_email():
    """Connect to the IMAP server and login."""
    if not all([IMAP_SERVER, EMAIL_USER, EMAIL_PASS]):
        logger.error("Email configuration is incomplete. Check environment variables.")
        sys.exit(1)
    
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        return mail
    except Exception as e:
        logger.error(f"Failed to connect to email server: {e}")
        sys.exit(1)

def build_search_query():
    """Build an IMAP search query to filter by allowed senders."""
    if not ALLOWED_SENDERS or ALLOWED_SENDERS[0] == '':
        logger.warning("No allowed senders specified. Will fetch all emails.")
        return 'ALL'
    
    # Build OR conditions for each sender
    or_conditions = []
    for sender in ALLOWED_SENDERS:
        sender = sender.strip()
        if sender:
            or_conditions.append(f'(FROM "{sender}")')
    
    if not or_conditions:
        return 'ALL'
    
    # Join with OR operator
    search_query = ' OR '.join(or_conditions)
    logger.info(f"Using search query: {search_query}")
    return search_query

def fetch_new_emails(mail, processed_ids):
    """Fetch new emails from allowed senders that haven't been processed yet."""
    mail.select('INBOX')
    
    # Build search query for allowed senders
    search_query = build_search_query()
    
    # Search for emails from allowed senders
    try:
        status, data = mail.search(None, search_query)
        if status != 'OK':
            logger.error(f"Failed to search inbox with query: {search_query}")
            return []
        
        email_ids = data[0].split()
        new_emails = [eid.decode() for eid in email_ids if eid.decode() not in processed_ids]
        
        logger.info(f"Found {len(new_emails)} new emails to process from allowed senders")
        return new_emails
    except Exception as e:
        logger.error(f"Error searching for emails: {e}")
        return []

def download_email(mail, email_id):
    """Download an email and save it as an .eml file."""
    status, data = mail.fetch(email_id.encode(), '(RFC822)')
    if status != 'OK':
        logger.error(f"Failed to fetch email {email_id}")
        return None
    
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email, policy=policy.default)
    
    # Get sender to include in filename
    from_header = msg.get('From', 'Unknown')
    # Extract email address or use the whole From header
    sender_match = re.search(r'<([^>]+)>', from_header)
    sender = sender_match.group(1) if sender_match else from_header
    sender = sanitize_filename(sender)
    
    # Create a filename based on subject, sender and date
    subject = msg.get('Subject', 'No Subject')
    date_str = msg.get('Date', datetime.now().strftime('%Y-%m-%dT%H_%M_%S'))
    
    # Try to parse the date for a consistent format
    try:
        date_obj = email.utils.parsedate_to_datetime(date_str)
        date_str = date_obj.strftime('%Y-%m-%dT%H_%M_%S')
    except:
        # If parsing fails, clean up the date string to make it filename-safe
        date_str = re.sub(r'[\\/*?:"<>|]', '_', date_str)
    
    filename = sanitize_filename(f"{sender}_{subject}_{date_str}.eml")
    filepath = os.path.join(EMAIL_STORAGE_DIR, filename)
    
    # Save the raw email
    with open(filepath, 'wb') as f:
        f.write(raw_email)
    
    logger.info(f"Downloaded email from {sender}: {subject}")
    return filepath

def process_new_emails():
    """Main function to connect, download, and process new emails."""
    logger.info("Starting email monitor process")
    
    # Load IDs of previously processed emails
    processed_ids = load_processed_ids()
    logger.info(f"Found {len(processed_ids)} previously processed emails")
    
    # Connect to email server
    mail = connect_to_email()
    
    try:
        # Fetch new emails from allowed senders
        new_email_ids = fetch_new_emails(mail, processed_ids)
        
        for email_id in new_email_ids:
            # Download the email
            email_path = download_email(mail, email_id)
            if email_path:
                # Mark as processed
                save_processed_id(email_id)
                
                # Optionally, you could call the extract_text_from_email function 
                # from extract_and_search.py here to process the email immediately
                
        logger.info(f"Processed {len(new_email_ids)} new emails")
        
    except Exception as e:
        logger.error(f"Error during email processing: {e}")
    finally:
        # Logout and close connection
        try:
            mail.logout()
        except:
            pass
    
    logger.info("Email monitor process completed")

if __name__ == "__main__":
    process_new_emails()