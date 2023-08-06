from dotenv import load_dotenv
import discord
import os
import random
import datetime
from PIL import Image
from discord.ext import tasks

load_dotenv()
intents = discord.Intents.default()
client = discord.Client(intents=intents)

def random_file(dir: str) -> str:
    if not os.path.isdir(dir):
        raise ValueError("The provided path is not a valid directory.")

    file_list = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    if not file_list:
        raise ValueError("The directory does not contain any files.")

    random_file_name = random.choice(file_list)
    random_file_path = os.path.join(dir, random_file_name)
    return random_file_path

def get_image_date(image_path: str) -> datetime.date:
    img = Image.open(image_path)
    
    exif_data = img._getexif()
    if exif_data:
        date_taken_tag = 36867 # Tag for 'DateTimeOriginal'            
        date_taken_str = exif_data.get(date_taken_tag)
        if date_taken_str:
            date_taken = datetime.datetime.strptime(date_taken_str, '%Y:%m:%d %H:%M:%S').date()
            return date_taken


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    send_photo.start()

@tasks.loop(hours=24)
async def send_photo():
    print('sending photo to channel')
    file_path = random_file('photos')
    date = get_image_date(file_path)

    channel_id = os.getenv('DEV_CHANNEL_ID')    
    channel = await client.fetch_channel(channel_id)

    if date is not None:
        await channel.send(date.strftime("%b %d %Y"))
    else:
        await channel.send('Date unknown')
    await channel.send(file=discord.File(file_path))

token = os.getenv('TOKEN')
client.run(token)

