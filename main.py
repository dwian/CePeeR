import discord

import os
from dotenv import load_dotenv

intents = discord.Intents.default()

bot = discord.Bot(
	intents=intents,
	debug_guilds=[1411053261183520858])


@bot.event
async def on_ready():
    print(f"{bot.user} ist online")


if __name__ == "__main__":
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            ##print(f"{filename} geladen")
            bot.load_extension(f"cogs.{filename[:-3]}")

    load_dotenv()
    bot.run(os.getenv("TOKEN"))