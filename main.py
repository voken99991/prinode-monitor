import discord
import aiohttp
import asyncio
import requests

TOKEN = "OTgyOTYxNDcwNDkwOTQ3NjI0.GDdDp6.EoQzpXprQ8F6Lzl3lZrpaC7DJoZEf8GAD36BsA"   # secondary bot
BOT_ID = 1413966238861754439        # your main bot’s user ID
WEBHOOK_URL = "https://discord.com/api/webhooks/1419385196595118190/qzWAPWs2ZYzThELIvTB6YUKeQzJT6LwTOqfCjMA2wNjpNu9rTpJAQIi2T6v2wUoOD71l"   # webhook for status alerts

client = discord.Client(intents=discord.Intents.default())
last_status = None

async def check_status():
    global last_status
    url = f"https://discord.com/api/v10/users/{BOT_ID}/profile"
    headers = {"Authorization": f"Bot {TOKEN}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                status = "online"
            else:
                status = "offline"

    if status != last_status:
        if status == "online":
            requests.post(WEBHOOK_URL, json={"content": "✅ Main bot is **online**"})
        else:
            requests.post(WEBHOOK_URL, json={"content": "❌ Main bot is **offline**"})
        last_status = status

@client.event
async def on_ready():
    print(f"Monitor bot logged in as {client.user}")
    while True:
        await check_status()
        await asyncio.sleep(30)  # check every 30s

client.run(TOKEN)
