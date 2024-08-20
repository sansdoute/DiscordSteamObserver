import discord
from discord.ext import commands, tasks
from steam_schnittstelle import getUserInfo
from database import fetchStartdataDB
from database import checkDifferences


TOKEN = ''

# Define the intents your bot will use
intents = discord.Intents.default()
intents.message_content = True  # Enable this if you want to receive message content events

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    # Start the background task
    fetchStartdataDB()
    check_steam_data.start()

async def send_message(channel_id: int, name: str):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(f"{name} went online!")
    else: 
        print("Channel not found")


#checks every minute for updates
@tasks.loop(minutes=1)
async def check_steam_data():
    try:
        toSend = checkDifferences()
        print(toSend)
        for person in toSend:
            name = person['response']['players'][0]['personaname']
            await send_message(956919040834691104, name)
        
            #print("Error in task.loop")
    except Exception as e:
        print(f"Error in task.loop: {e}")


#register a new User to db
@bot.command(name='register')
async def register(ctx, discord_id: str, steam_id: str):
    getUserInfo(discord_id, steam_id)


# Run the bot with the token
bot.run(TOKEN)

