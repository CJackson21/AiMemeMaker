import requests
import json
import random as r
import discord
from discord.ext import commands

id = 0
response = requests.get("https://api.imgflip.com/get_memes")
token = ''
intents = discord.Intents.default()
intents.typing = False  # You can customize which events you want to listen to
bot = commands.Bot(command_prefix='!', intents=intents)


last_messages = []
holder = []

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')

@bot.event
async def on_message(message):
    # Check if the message is from a bot to avoid responding to other bots
    if message.author.bot:
        return

    # Append the last message to the list for this channel
    last_messages.append((message.channel.id, message))
    holder.append(message)

    # Check if the message starts with the bot's prefix
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)

# Custom command to retrieve the last message
@bot.command()
async def get_last(ctx):
    # Get the last message from the same channel
    last_message = None
    for channel_id, message in reversed(last_messages):
        if channel_id == ctx.channel.id:
            last_message = message
            holder.append(last_message)
            break

    if last_message:
        await ctx.send(f"The last message was: {last_message.content}")
    else:
        await ctx.send("No previous message found in this channel.")



# Check for errors in the response
if response.status_code == 200:
    try:
        meme_templates = response.json()["data"]["memes"]
        
        # Extract and print the template_ids
        template_ids = [template["id"] for template in meme_templates]
        print(template_ids)
        id = r.choice(template_ids)
        print("Template IDs:")
        
    except KeyError:
        print("Error: Unexpected JSON structure in the API response.")
else:
    print(f"Error: API request failed with status code {response.status_code}")

def split_sentence_in_half():
    if holder:
        message = holder[-1]  # Get the last message from the list
        content = message.content  # Extract the content from the message
        middle = len(content) // 2
        while middle < len(content) and content[middle] != " ":
            middle += 1
        print(middle)
        first_half = content[:middle]
        second_half = content[middle:]
        print(second_half)
        return first_half, second_half
    else:
        return None, None


# Example usage:
top_text, bottom_text = split_sentence_in_half()

# Define the meme text and template
# top_text = "This is the top text"
# bottom_text = "This is the bottom text"
template_id = id

# Define the request parameters as a dictionary
params = {
    "template_id": id,
    "username": "cjackson15",
    "password": "TeamFly14!",
    "text0": top_text,
    "text1": bottom_text
}

# Make a request to the Imgflip API using form-url-encoded parameters
response = requests.post("https://api.imgflip.com/caption_image", data=params)

# Check for errors in the response
if response.status_code == 200:
    try:
        # Pretty print the JSON response to explore its structure
        print(json.dumps(response.json(), indent=4))
    except KeyError:
        print("Error: Unexpected JSON structure in the API response.")
else:
    print(f"Error: API request failed with status code {response.status_code}")

bot.run(token)

