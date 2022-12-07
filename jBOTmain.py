import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get

# Replace YOUR_TOKEN_HERE with your Discord bot token
TOKEN = 'MTA0OTk4MzQ5MzI4OTAyOTY4Mw.GsK85b.5xExKrUPVfX-HY5AQtYdMoknjHvTGaAp2CV5xI'
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

# Run the bot using the token
bot.run(TOKEN)