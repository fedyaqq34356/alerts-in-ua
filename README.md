# Air Raid Alert Monitor

A Python-based monitoring system that tracks air raid alerts for Dnipro, Ukraine and sends real-time notifications to a Telegram channel.

> **Note**: This bot is configured for Dnipro region as requested by the client. See [Multi-Region Setup](#multi-region-setup) to monitor multiple regions or all of Ukraine.

## Features

- **Real-time monitoring**: Checks alert status at configurable intervals
- **Telegram notifications**: Automatic messages when alerts start and end
- **Status tracking**: Monitors alert states (active, partial, no alert)
- **Logging**: Comprehensive logging to file and console
- **Error handling**: Graceful error management for API failures
- **Configurable**: Easy customization via environment variables

## Requirements

- Python 3.8+
- Telegram Bot Token
- Alerts in UA API Token
- Telegram Channel ID

## Installation

1. **Clone the repository**:

```bash
git clone https://github.com/YOUR_USERNAME/air-raid-alert-monitor.git
cd air-raid-alert-monitor
```

2. **Create virtual environment**:

```bash
python -m venv venv
```

3. **Activate virtual environment**:

Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

4. **Install dependencies**:

```bash
pip install -r requirements.txt
```

5. **Configure environment variables**:

Create a `.env` file in the project root:

```env
ALERTS_API_TOKEN=your_alerts_api_token_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHANNEL_ID=@your_channel_id
DNIPRO_UID=44
CHECK_INTERVAL=30
LOG_FILE=alert.log
```

### Getting API Tokens

**Alerts in UA API**:
1. Visit [alerts.in.ua](https://alerts.in.ua/)
2. Register and obtain your API token

**Telegram Bot**:
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Create a new bot with `/newbot`
3. Copy the bot token
4. Add your bot to your channel as administrator

**Channel ID**:
- For public channels: use `@channelname`
- For private channels: use the numeric ID (e.g., `-1001234567890`)

## Usage

Run the monitor:

```bash
python main.py
```

The application will:
1. Connect to the Alerts in UA API
2. Monitor alert status for Dnipro
3. Send notifications to your Telegram channel when alerts start or end
4. Log all activity to console and log file

To stop the monitor, press `Ctrl+C`.

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ALERTS_API_TOKEN` | API token from alerts.in.ua | Required |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token from BotFather | Required |
| `TELEGRAM_CHANNEL_ID` | Telegram channel ID or username | Required |
| `DNIPRO_UID` | Region UID for Dnipro | 332 |
| `CHECK_INTERVAL` | Check interval in seconds | 30 |
| `LOG_FILE` | Log file path | alert.log |

### Customizing Messages

Edit `messages.py` to customize notification text:

```python
MESSAGES = {
    'start': "🚨 Air raid alert\nPlease go to shelter",
    'end': "✅ Air raid alert ended\nYou can leave the shelter"
}
```

## Project Structure

```
air-raid-alert-monitor/
├── main.py                 # Entry point and main loop
├── api_client.py          # Alerts API client
├── telegram_sender.py     # Telegram bot integration
├── config.py              # Configuration loader
├── logger.py              # Logging setup
├── messages.py            # Notification messages
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
└── README.md             # This file
```

## How It Works

1. **Initialization**: Loads configuration from `.env` file
2. **Monitoring Loop**: 
   - Fetches current alert status from Alerts in UA API
   - Compares with previous status
   - Detects status changes (alert started/ended)
3. **Notifications**: Sends formatted messages to Telegram channel with timestamp
4. **Logging**: Records all events to log file and console

### Alert States

- `no_alert` - No active alerts
- `active` - Alert is active
- `partly` - Partial alert
- `error` - API error occurred

## Dependencies

- `alerts_in_ua` - Official Python client for Alerts in UA API
- `aiogram` - Telegram Bot API framework
- `python-dotenv` - Environment variable management

## Troubleshooting

### Bot doesn't send messages

- Ensure bot is added as administrator to your channel
- Verify `TELEGRAM_CHANNEL_ID` format is correct
- Check bot token is valid

### API errors

- Verify `ALERTS_API_TOKEN` is valid and active
- Check your internet connection
- Ensure the Alerts in UA API is accessible

### Python module errors

- Reinstall dependencies: `pip install -r requirements.txt --upgrade`
- Check Python version: `python --version` (3.8+ required)

## Multi-Region Setup

By default, the bot monitors only **Dnipro region** as requested by the client. To monitor **all regions of Ukraine**:

### Step 1: Update `api_client.py`

Replace the entire file with:

```python
from alerts_in_ua import AsyncClient
from config import ALERTS_API_TOKEN

async def get_all_alert_statuses():
    client = AsyncClient(ALERTS_API_TOKEN)
    statuses = await client.get_air_raid_alert_statuses_by_oblast()
    if not statuses:
        return None
    return {status.location_title: status.status for status in statuses}
```

### Step 2: Update `main.py`

Replace lines 9-44 (from `last_status = None` to the end of `check_and_notify` function) with:

```python
last_statuses = {}  # Dictionary to store previous statuses by region

STATUS_ICONS = {
    'active': '🚨',
    'partly': '⚠️',
    'no_alert': '✅'
}

async def check_and_notify():
    global last_statuses
    current_statuses = await get_all_alert_statuses()
    
    if current_statuses is None:
        logger.error("Ошибка получения статусов")
        return
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    for region, current in current_statuses.items():
        last = last_statuses.get(region, None)
        
        if last is None:
            last_statuses[region] = current
            logger.info(f"Начальный статус для {region}: {current}")
            continue
        
        if last != current:
            if current in ['active', 'partly'] and last == 'no_alert':
                message_template = MESSAGES['start'] if current == 'active' else MESSAGES.get('partial', MESSAGES['start'])
                message = f"{message_template.format(region=region)}\n\n{timestamp}"
                await send_message_to_channel(message)
                logger.info(f"Тревога в {region}")
            
            elif current == 'no_alert' and last in ['active', 'partly']:
                message = f"{MESSAGES['end'].format(region=region)}\n\n{timestamp}"
                await send_message_to_channel(message)
                logger.info(f"Отбой в {region}")
            
            last_statuses[region] = current
```

### Step 3: Update `messages.py`

Replace with:

```python
MESSAGES = {
    'start': "🚨 Повітряна тривога в {region}\nПросимо пройти в укриття",
    'end': "✅ Відбій повітряної тривоги в {region}\nМожна залишати укриття",
    'partial': "⚠️ Часткова тривога в {region}"
}
```

### Step 4: Update `.env` (optional)

Remove the `DNIPRO_UID` line as it's no longer needed:

```env
ALERTS_API_TOKEN=your_alerts_api_token_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHANNEL_ID=@your_channel_id
CHECK_INTERVAL=30
LOG_FILE=alert.log
```

### Step 5: Update `config.py`

Remove line 9 (`DNIPRO_UID = int(os.getenv("DNIPRO_UID", 332))`).

---

**That's it!** The bot will now monitor all regions of Ukraine and send notifications for each region separately.

## License

GNU General Public License v3.0 - see LICENSE file for details.

## Acknowledgments

- [Alerts in UA](https://alerts.in.ua/) for providing the alert API
- [aiogram](https://github.com/aiogram/aiogram) for Telegram bot framework

---

Built with Python, Aiogram, and APScheduler.