import discord
from discord.ext import commands, tasks
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    send_message.start()

@tasks.loop(minutes=5)
async def send_message():
    channel = bot.get_channel(os.getenv('DEV_CHANNEL_ID'))  # Replace YOUR_CHANNEL_ID with the actual channel ID
    await channel.send("This is a message sent every 5 minutes.")

@send_message.before_loop
async def before_send_message():
    await bot.wait_until_ready()

asyncio.run(bot.run(os.getenv('TOKEN')))
