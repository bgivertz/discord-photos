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
    # Check if the directory exists
    if not os.path.isdir(dir):
        raise ValueError("The provided path is not a valid directory.")

    # Get a list of all files in the directory
    file_list = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]

    # Check if there are any files in the directory
    if not file_list:
        raise ValueError("The directory does not contain any files.")

    # Choose a random file from the list
    random_file_name = random.choice(file_list)

    # Construct the full path to the randomly chosen file
    random_file_path = os.path.join(dir, random_file_name)

    return random_file_path

def get_image_date(image_path: str) -> datetime.date:
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Get the image's Exif data
        exif_data = img._getexif()
        
        if exif_data:
            # Get the tag for the date and time the photo was taken (36867 represents 'DateTimeOriginal')
            date_taken_tag = 36867
            
            # Retrieve the date and time as a string
            date_taken_str = exif_data.get(date_taken_tag)
            if date_taken_str:
                # Convert the date string to a datetime object
                date_taken = datetime.datetime.strptime(date_taken_str, '%Y:%m:%d %H:%M:%S').date()
                return date_taken
            else:
                return None  # Date not found in metadata
        
        else:
            return None  # No Exif data found
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Error occurred


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

