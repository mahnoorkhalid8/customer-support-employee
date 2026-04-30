"""
Email Auto-Check Service
Automatically checks and responds to emails every 5 minutes
"""
import asyncio
import aiohttp
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_URL = "http://localhost:8001"
CHECK_INTERVAL = 300  # 5 minutes in seconds

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/email_autocheck.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


async def check_emails():
    """Check and respond to emails via API"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/gmail/check-emails") as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"✅ Email check successful: {data.get('status', 'Processing')}")
                    return True
                else:
                    logger.error(f"❌ Email check failed with status {response.status}")
                    return False
    except Exception as e:
        logger.error(f"❌ Error checking emails: {e}")
        return False


async def check_api_health():
    """Check if API server is running"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/health", timeout=aiohttp.ClientTimeout(total=5)) as response:
                if response.status == 200:
                    return True
                return False
    except Exception:
        return False


async def main():
    """Main loop - checks emails every 5 minutes"""
    logger.info("🚀 Email Auto-Check Service Started")
    logger.info(f"📧 Checking emails every {CHECK_INTERVAL // 60} minutes")
    logger.info(f"🔗 API URL: {API_URL}")

    # Wait for API to be ready
    logger.info("⏳ Waiting for API server to be ready...")
    while not await check_api_health():
        logger.warning("API server not ready, retrying in 10 seconds...")
        await asyncio.sleep(10)

    logger.info("✅ API server is ready!")

    # Main loop
    check_count = 0
    while True:
        try:
            check_count += 1
            logger.info(f"\n{'='*60}")
            logger.info(f"📬 Email Check #{check_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"{'='*60}")

            success = await check_emails()

            if success:
                logger.info(f"✅ Check #{check_count} completed successfully")
            else:
                logger.warning(f"⚠️ Check #{check_count} had issues")

            logger.info(f"⏰ Next check in {CHECK_INTERVAL // 60} minutes...")
            await asyncio.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            logger.info("\n🛑 Service stopped by user")
            break
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            logger.info("⏰ Retrying in 1 minute...")
            await asyncio.sleep(60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n👋 Email Auto-Check Service Stopped")
