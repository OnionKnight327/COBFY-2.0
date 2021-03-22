import discord
from discord.ext import commands
import youtube_dl
import os
import random

client = commands.Bot(command_prefix="?")
token = 'ODE0NjU5NjMwNjg3ODQ2NDQy.YDhE5w.fp8WK6ESFU9ifxOdCWS5SfLkqlk'

music_list = ["https://www.youtube.com/watch?v=RSodZmM0HnE&ab_channel=FZA"]


#Function to play music
async def run(ctx, track):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Whoa, too fast there, buddy. Slow down.")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect() #COBFY has to be in a voice channel to recognize the "voice" variable
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([track])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))



@client.event
async def on_ready():
    print('Initialized')
        

@client.command()
async def amogus(ctx):
    await run(ctx, music_list[0])


# This command makes the bot leave the discord when commanded to #

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("I have to be in a bot channel to leave one!")

# -------------------------------------------------------------- #


# This command adds a video to its playlist via a youtube URL    #

@client.command()
async def add(ctx, song):
    music_list.append(song)
    await ctx.send("Done! I just added your video to my playlist.")

# -------------------------------------------------------------- #


# This command should send a message of all the video in its personal playlist
@client.command()
async def playlist(ctx):
    max = (len(music_list))
    for i in range(0, max):
       await ctx.send(music_list[i])
# -------------------------------------------------------------- #

# This command shuffles and plays a song along its personal playlist #

@client.command()
async def shuffle(ctx):
    randomnumber = random.randint(0, (len(music_list)-1))
    choice = music_list[randomnumber]
    await run(ctx, choice)

# Yeah I know the code uses the exact same one as the amogus command. I'm hoping to consolidate this into one function. #

# This command can play any one song by given a url
@client.command()
async def play(ctx, url):
    await run(ctx, url)
    ctx.send("Enjoy :)")
# ------------------------------------------------ #


client.run(token)