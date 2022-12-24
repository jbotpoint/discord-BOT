import discord
import youtube_dl
import random
import requests
from discord.ext import commands
from discord.utils import get
import openai
import os
import re


#contains the discord bot's token
import constants

# Replace YOUR_TOKEN_HERE with your Discord bot token
TOKEN = constants.TOKEN_CONST

#Open AI API token
OPENAI_TOKEN = constants.OPENAI_TOKEN

#api_client = openai.API(OPENAI_TOKEN)
openai.api_key = OPENAI_TOKEN

intents = discord.Intents.all()
# Create a Discord client
client = discord.Client(intents=discord.Intents.default())

# Create a Discord bot using the '!' command prefix
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def movielist(ctx):
    embed = discord.Embed(title="Movie Watch List", color=discord.Colour.purple())
    embed.set_thumbnail(url="https://archive.org/download/png-movie-ticket-movie-ticket-1-950/png-movie-ticket-movie-ticket-1-950.png")
    with open("movie_list.txt", "r") as filedata:
        filelines = filedata.readlines()
    for line in filelines:
        if line == "":
            continue
        strlist = line.split("|", 1)
        mname = strlist[0]
        mlink = "No Link"
        print(strlist)
        if re.search("(?P<url>https?://[^\s]+)", strlist[1]):
            mlink = strlist[1]
        embed.add_field(name=mname, value=mlink, inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def addmovie(ctx):
    msgcontent = ctx.message.content
    stringlist = re.split("(?P<url>https?://[^\s]+)", msgcontent)
    listsize = len(stringlist)

    print(stringlist)

    movie_name = stringlist[0].split(" ", 1)[1]
    movie_link = ""
    if listsize >= 2:
        movie_link = stringlist[1]
    
    f = open("movie_list.txt", "a")
    f.write(movie_name + "|" + movie_link + "\n")
    f.close()

    await ctx.message.add_reaction('✅')

@bot.command()
async def delmovie(ctx):
    msgcontent = ctx.message.content.split(" ", 1)
    movie_name = msgcontent[1]

    with open("movie_list.txt", 'r') as filedata:
        inputFilelines = filedata.readlines()
        lineindex = 1
        for i in range(len(inputFilelines)):
            if re.search(movie_name, inputFilelines[int(i)]):
                line_to_delete = i+1
                break
    with open("movie_list.txt", 'w') as filedata:
        for textline in inputFilelines:
            if lineindex != line_to_delete:
                filedata.write(textline)
            lineindex += 1
    
    await ctx.message.add_reaction('✅')   

@bot.command(pass_context=True)
async def ask(ctx):
    msgcontent = ctx.message.content.split(" ", 1)
    response = openai.Completion.create(
        prompt=msgcontent[1],
        max_tokens=256,
        model="text-davinci-003",
        temperature=0.9
    )
    await ctx.send(response["choices"][0]["text"])

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

    value1 = random.randint(1, 50)
    value2 = random.randint(1, 50)
    emojVal = value1 % 10
    if value1 == value2:
        if emojVal == 1:
            emoji = '🤪'
        elif emojVal == 2:
            emoji = '🤥'
        elif emojVal == 3:
            emoji = '🥺'
        elif emojVal == 4:
            emoji = '😡'
        elif emojVal == 5:
            emoji = '💀'
        elif emojVal == 6:
            emoji = '😈'
        elif emojVal == 7:
            emoji = '😂'
        elif emojVal == 8:
            emoji = '😘'
        else:
            emoji = '😊'
        try:
            await message.add_reaction(emoji)
        except discord.HTTPException:
            pass
    if message.content[0] == '!':
        await bot.process_commands(message)
    
    
    
# Run the bot using the token
bot.run(TOKEN)
