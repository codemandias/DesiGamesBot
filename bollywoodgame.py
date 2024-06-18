import discord
import random
import json
from dotenv import load_dotenv
import os
load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
MOVIES_FILE = 'movies.json'
BOLLYWOOD = "BOLLYWOOD"

intents = discord.Intents.default()
intents.message_content = True  # This allows the bot to read message content

client = discord.Client(intents=intents)

# Load movie data from JSON file
def load_movies():
    try:
        with open(MOVIES_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        return []

movies_data = load_movies()  # Load movie data at the start
movies = [movie["Title"].upper() for movie in movies_data]

# Initialize hint tracking dictionary
hint_used = {}

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!playbw'):
        # Choose a random movie
        movie_index = random.randint(0, len(movies) - 1)
        movie_title = movies[movie_index]
        movie_details = movies_data[movie_index]

        # Prepare the masked movie name
        masked_name = ' '.join(['_' if ch != ' ' else '  ' for ch in movie_title])

        # Initialize game state
        guesses = set()
        wrong_attempts = 0
        max_attempts = 9

        # Prepare initial message
        await message.channel.send(f"Let's play Bollywood Movie Guessing Game!\nMovie: `{masked_name}`")

        def display_movie():
            return ' '.join([ch if ch in guesses else '_' if ch != ' ' else '  ' for ch in movie_title])

        def display_progress():
            return f"{display_movie()}"

        def display_bollywood():
            strikethrough = '~~'
            return ''.join([strikethrough + ch + strikethrough if i < wrong_attempts else ch for i, ch in enumerate(BOLLYWOOD)])

        # Reset hint tracking for new game
        hint_used.clear()

        while wrong_attempts < max_attempts:
            response = await client.wait_for('message')

            if response.author == message.author:
                if response.content.lower() == '!hint':
                    # Filter out the "Title" key from possible hints and avoid repeating hints
                    hint_choices = {key: value for key, value in movie_details.items() if key != "Title" and key not in hint_used}
                    if hint_choices:
                        hint_key, hint_value = random.choice(list(hint_choices.items()))
                        hint_used[hint_key] = hint_value  # Track used hint
                        await message.channel.send(f"Hint - {hint_key}: {hint_value}")
                    else:
                        await message.channel.send("No more hints available.")
                else:
                    guess = response.content.upper()

                    if len(guess) == 1 and guess.isalpha():
                        if guess in guesses:
                            await message.channel.send(f"You've already guessed '{guess}'. Guess another letter.")
                        else:
                            guesses.add(guess)
                            if guess in movie_title:
                                await message.channel.send(f"Correct! `{display_progress()}`")
                                if '_' not in display_movie():
                                    await message.channel.send(f"Congratulations! You guessed the movie: **{movie_title}**")
                                    break
                            else:
                                wrong_attempts += 1
                                if wrong_attempts < max_attempts:
                                    await message.channel.send(f"Wrong guess! {display_bollywood()}")
                                if wrong_attempts == max_attempts:
                                    await message.channel.send(f"Game over! The movie was **{movie_title}**.\n{display_bollywood()}")
                                    break
                    else:
                        await message.channel.send("Invalid input. Please enter a single letter.")

        await message.channel.send("Game ended. Type `!playbw` to start a new game.")

client.run(TOKEN)