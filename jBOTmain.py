import discord
import youtube_dl
import random
from discord.ext import commands
from discord.utils import get


#contains the discord bot's token
import constants

# Replace YOUR_TOKEN_HERE with your Discord bot token
TOKEN = constants.TOKEN_CONST

intents = discord.Intents.all()
# Create a Discord client
client = discord.Client(intents=discord.Intents.default())

# Create a Discord bot using the '!' command prefix
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def disconnect(ctx):
    await ctx.voice_client.disconnect()   

@bot.command(pass_context=True)
async def play(ctx, url):
    # Join the voice channel that the user is in
    user_voice_channel = ctx.author.voice.channel
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format' : 'bestaudio'}
    voice_client = await user_voice_channel.connect()

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        voice_client.play(source)

@bot.event
async def on_message(message):

    value1 = random.randint(1, 10)
    value2 = random.randint(1, 10)

    if value1 == value2:
        if value1 == 1:
            emoji = '🤪'
        elif value1 == 2:
            emoji = '🤥'
        elif value1 == 3:
            emoji = '🥺'
        elif value1 == 4:
            emoji = '😡'
        elif value1 == 5:
            emoji = '💀'
        elif value1 == 6:
            emoji = '😈'
        elif value1 == 7:
            emoji = '😂'
        elif value1 == 8:
            emoji = '😘'
        else:
            emoji = '😊'
        try:
            await message.add_reaction(emoji)
        except discord.HTTPException:
            pass
    
# Run the bot using the token
bot.run(TOKEN)
