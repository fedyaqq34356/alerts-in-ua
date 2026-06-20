import asyncio
from datetime import datetime
from config import DNIPRO_UID, CHECK_INTERVAL
from logger import setup_logging
from messages import MESSAGES
from api_client import get_alert_status
from telegram_sender import send_message_to_channel

logger = setup_logging()

last_status = None

async def check_and_notify():
    global last_status
    current = await get_alert_status(DNIPRO_UID)
    
    if current == 'error':
        logger.error("Ошибка получения статуса")
        return
    
    if last_status is None:
        last_status = current
        logger.info(f"Начальный статус: {current}")
        return
    
    if last_status != current:
        timestamp = datetime.now().strftime("%H:%M:%S")
        if current in ['active', 'partly'] and last_status == 'no_alert':
            message = f"{MESSAGES['start']}\n\n{timestamp}"
            await send_message_to_channel(message)
            logger.info("Тревога начата")
        
        elif current == 'no_alert' and last_status in ['active', 'partly']:
            message = f"{MESSAGES['end']}\n\n{timestamp}"
            await send_message_to_channel(message)
            logger.info("Тревога отменена")
        
        last_status = current

async def main():
    logger.info(f"Мониторинг Днепра (UID: {DNIPRO_UID}, интервал: {CHECK_INTERVAL}с)")
    try:
        while True:
            await check_and_notify()
            await asyncio.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        logger.info("Остановлено")

if __name__ == "__main__":
    asyncio.run(main())