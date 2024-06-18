import discord
from dotenv import load_dotenv
import os

from bollygame import setup_bollywood_game
from hollygame import setup_hollywood_game


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!playbw'):
        await setup_bollywood_game(client, message)  # Pass client as an argument

    if message.content.startswith('!playhw'):
        await setup_hollywood_game(client, message)  # Pass client as an argument


client.run(TOKEN)