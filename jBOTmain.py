import discord
import youtube_dl
import random
from discord.ext import commands
from discord.utils import get
import openai
import re
import tierlistparser
import asyncio


#contains the discord bot's token
import constants

# Replace YOUR_TOKEN_HERE with your Discord bot token
TOKEN = constants.TOKEN_CONST

#Open AI API token
OPENAI_TOKEN = constants.OPENAI_TOKEN

#api_client = openai.API(OPENAI_TOKEN)
openai.api_key = OPENAI_TOKEN

tierlistObj = tierlistparser.parse_tier_file("tierlistData.txt")

intents = discord.Intents.all()
# Create a Discord client
client = discord.Client(intents=discord.Intents.default())

# Create a Discord bot using the '!' command prefix
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def assigntier(ctx):
    msgcontent = ctx.message.content.split(" ")
    if len(msgcontent) > 3 or len(msgcontent) < 2:
        await ctx.message.add_reaction('❌')
        return

    tier = msgcontent[1]

    def check(m):
        return m.channel == ctx.message.channel and m.author == ctx.message.author
    await ctx.send("Value of Tier?")
    try:
        msg = await bot.wait_for("message", timeout=60.0, check=check)
        #reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.message.add_reaction('❌')
        return

    value = msg.content

    with open("tierOrder.txt", "r") as filedata:
        index = -1
        lines = filedata.readlines()
        for i in range(len(lines)):
            if re.search(tier, lines[int(i)]):
                index = i+1
                break
    if index == -1:
        index = i+1
        tier = lines[int(i)] + tier
    with open("tierOrder.txt", "w") as filedata:
        lineindex = 1
        for line in lines:
            if lineindex != index:
                filedata.write(line)
            else:
                filedata.write(tier + "|" + value + "\n")
            lineindex += 1

    await msg.add_reaction('✅')

@bot.command()
async def unratemovie(ctx):
    msgcontent = ctx.message.content.split(" ", 1)
    if len(msgcontent) < 2:
        await ctx.message.add_reaction('❌')
        return
    
    movie_name = msgcontent[1]
    for tier in list(tierlistObj):
        if movie_name in tierlistObj[tier]:
            tierlistObj[tier].remove(movie_name)
            if not tierlistObj[tier]:
                tierlistObj.pop(tier, None)
                with open("tierOrder.txt", "r") as filedata:
                    index = -1
                    lines = filedata.readlines()
                    for i in range(len(lines)):
                        if re.search(tier, lines[int(i)]):
                            index = i+1
                            break

                with open("tierOrder.txt", "w") as filedata:
                    lineindex = 1
                    for line in lines:
                        if lineindex != index:
                            filedata.write(line)
                        lineindex += 1

    with open("tierlistData.txt") as filedata:
        inputFilelines = filedata.readlines()
        lineindex = 1
        line_to_delete = []
        for i in range(len(inputFilelines)):
            if re.search(movie_name, inputFilelines[int(i)]):
                line_to_delete.append(i+1)
    if not line_to_delete:
        await ctx.message.add_reaction('❌')
        return

    with open("tierlistData.txt", 'w') as filedata:
        for textline in inputFilelines:
            if lineindex not in line_to_delete:
                filedata.write(textline)
            lineindex += 1

    await ctx.message.add_reaction('✅')

@bot.command()
async def deltier(ctx):
    msgcontent = ctx.message.content.split(" ", 1)
    if len(msgcontent) < 2:
        await ctx.message.add_reaction('❌')
        return
    tier = msgcontent[1]
    if not tier in tierlistObj:
        await ctx.message.add_reaction('❌')
        return

    with open("tierlistData.txt", "r") as filedata:
        inputFilelines = filedata.readlines()
        lineindex = 1
        line_to_delete = []
        for i in range(len(inputFilelines)):
            if re.search("\|" + tier, inputFilelines[int(i)]):
                line_to_delete.append(i+1)

    print(line_to_delete)
    with open("tierlistData.txt", 'w') as filedata:
        for textline in inputFilelines:
            if not lineindex in line_to_delete:
                filedata.write(textline)
            lineindex += 1
    tierlistObj.pop(tier, None)

    with open("tierOrder.txt", "r") as filedata:
        index = -1
        lines = filedata.readlines()
        for i in range(len(lines)):
            if re.search(tier, lines[int(i)]):
                index = i+1
                break

    with open("tierOrder.txt", "w") as filedata:
        lineindex = 1
        for line in lines:
            if lineindex != index:
                filedata.write(line)
            lineindex += 1


    await ctx.message.add_reaction('✅')

@bot.command()
async def tierlist(ctx):
    msgcontent = ctx.message.content.split(" ", 1)
    if len(msgcontent) < 2:
        tier = "all"
    else:    
        tier = msgcontent[1]
    if tier == "all":
        sorted_keys = sorted(tierlistObj, key=tierlistparser.custom_sort)
        embed = discord.Embed(title="All Tiers", color=discord.Colour.random())
        embed.set_thumbnail(url="https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/61214/podium-trophies-clipart-xl.png")
        for dictTier in sorted_keys:
            value_to_embed = ""
            for movie in tierlistObj[dictTier]:
                if value_to_embed == "":
                    value_to_embed = movie
                else:
                    value_to_embed = value_to_embed + ", " + movie
            embed.add_field(name=dictTier, value=value_to_embed, inline=False)
    else:
        if not tier in tierlistObj:
           await ctx.message.add_reaction('❌')
           return

        embed = discord.Embed(title=f"{tier} Tier", color=discord.Colour.random())
        embed.set_thumbnail(url="https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/61214/podium-trophies-clipart-xl.png")

        for movie in tierlistObj[tier]:
            embed.add_field(name=movie, value="\u200b", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def ratemovie(ctx):
    msgcontent = ctx.message.content.split(" ", 1)
    if len(msgcontent) > 1:
        movie_name = msgcontent[1]
    else:
        movie_name = ""
    if movie_name == "":
        await ctx.message.add_reaction('❌')
        return

    def check(m):
        return m.channel == ctx.message.channel and m.author == ctx.message.author

    await ctx.send("Tier?")
    try:
        msg = await bot.wait_for("message", timeout=60.0, check=check)
        #reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.message.add_reaction('❌')
        return

    movie_tier = msg.content
    if movie_tier == "" or movie_tier == " ":
        await ctx.message.add_reaction('❌')
        return
    try:
        tierlistObj[movie_tier].append(movie_name)
    except KeyError:
        tierlistObj[movie_tier] = [movie_name]
        f2 = open("tierOrder.txt", "a")
        f2.write(movie_tier + "|" + "1000" + "\n")
        f2.close()
        
    f = open("tierlistData.txt", "a")
    f.write(movie_name + "|" + movie_tier + "\n")
    f.close()

    await msg.add_reaction('✅')
    
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
        if mname == "":
            mname = "No Title"
        mlink = "No Link"

        if re.search("(?P<url>https?://[^\s]+)", strlist[1]):
            mlink = strlist[1]
        embed.add_field(name=mname, value=mlink, inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def addmovie(ctx):
    msgcontent = ctx.message.content
    stringlist = re.split("(?P<url>https?://[^\s]+)", msgcontent)
    listsize = len(stringlist)

    movie_name = stringlist[0].split(" ", 1)[1]
    movie_link = ""
    if listsize >= 2:
        movie_link = stringlist[1]
    
    if movie_name == "":
        await ctx.message.add_reaction('❌')
        return
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
        line_to_delete = -1
        for i in range(len(inputFilelines)):
            if re.search(movie_name, inputFilelines[int(i)]):
                line_to_delete = i+1
                break
    if line_to_delete == -1:
        await ctx.message.add_reaction('❌')
        return

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
    if message.content:
        if message.content[0] == '!':
            await bot.process_commands(message)
    
    
    
# Run the bot using the token
bot.run(TOKEN)
