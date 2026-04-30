"""
Automatic Email Checker for Gmail FTE
Polls Gmail inbox every 30 seconds and processes new emails with AI responses
"""
import time
import requests
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

API_BASE_URL = "http://localhost:8001"
CHECK_INTERVAL = 30  # seconds

def check_emails():
    """Trigger email check via API"""
    try:
        response = requests.get(f"{API_BASE_URL}/gmail/check-emails", timeout=5)
        if response.status_code == 200:
            logger.info("✓ Email check triggered successfully")
            return True
        else:
            logger.error(f"✗ Email check failed: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"✗ Error checking emails: {e}")
        return False

def check_status():
    """Check Gmail connection status"""
    try:
        response = requests.get(f"{API_BASE_URL}/gmail/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("status") == "connected"
        return False
    except:
        return False

def main():
    """Main loop"""
    logger.info("=" * 60)
    logger.info("Gmail FTE Auto Email Checker Started")
    logger.info("=" * 60)
    logger.info(f"API URL: {API_BASE_URL}")
    logger.info(f"Check Interval: {CHECK_INTERVAL} seconds")
    logger.info("=" * 60)

    # Initial status check
    if check_status():
        logger.info("✓ Gmail connection: ACTIVE")
    else:
        logger.warning("✗ Gmail connection: INACTIVE")
        logger.warning("Please ensure the backend server is running")

    logger.info("\nStarting automatic email monitoring...")
    logger.info("Press Ctrl+C to stop\n")

    check_count = 0

    try:
        while True:
            check_count += 1
            logger.info(f"[Check #{check_count}] Checking for new emails...")

            if check_emails():
                logger.info("→ FTE will process any unread emails and send AI replies")

            logger.info(f"→ Next check in {CHECK_INTERVAL} seconds\n")
            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        logger.info("\n" + "=" * 60)
        logger.info("Email checker stopped by user")
        logger.info(f"Total checks performed: {check_count}")
        logger.info("=" * 60)

if __name__ == "__main__":
    main()
