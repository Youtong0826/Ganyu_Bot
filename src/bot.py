import asyncio
import os

from dotenv import load_dotenv

from discord import (
    Intents,
    Status,
    Activity,
    ActivityType
)

from core import Bot

load_dotenv()

intents = Intents.all()
intents.message_content = False
intents.presences = False

bot = Bot(
    command_prefix="g!",
    intents=intents
)

for folder in ["commands", "cogs", "events"]: 
    bot._load_extension(folder)

@bot.event
async def on_ready():
    print(">>Bot is online<<")
    print(f"-- Watching {len(bot.guilds)} guilds & {len(bot.users)} users ")

    async def run_activity_loop():

        names = [
            f"/help | {len(bot.guilds)} 個伺服器",
            f"/help | {len(bot.users)} 個用戶",
            f"/help | ping {round(bot.latency * 1000)} ms",
            f"/help | no message intent sad :("
        ]

        ACTIVITY_OPTION = {
            "status": Status.idle,
            "application_id": 921673886049910795,
            "type" : ActivityType.watching,
        }

        for i in names:
            await bot.change_presence(activity=Activity(name=i ,**ACTIVITY_OPTION))
            await asyncio.sleep(10.0)

    while True:
        await run_activity_loop()

if __name__ == "__main__":
    bot.run(os.environ.get("TOKEN"))
    #bot.run()

