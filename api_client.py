from alerts_in_ua import AsyncClient
from config import ALERTS_API_TOKEN

async def get_alert_status(uid: int):
    client = AsyncClient(ALERTS_API_TOKEN)
    status = await client.get_air_raid_alert_status(uid)
    return status.status if status else 'error'