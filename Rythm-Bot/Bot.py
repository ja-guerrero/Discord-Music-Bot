import os
import asyncio 
import discord
from dotenv import load_dotenv
from discord.ext import commands
from youtube_dl import YoutubeDL as ytdl
import re,requests,subprocess,urllib.parse,urllib.request
from bs4 import BeautifulSoup

import moviepy.editor as mp

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')


bot = commands.Bot(command_prefix='!') 

def get_audio(name):

	query_string = urllib.parse.urlencode({"search_query":name})

	formatUrl = urllib.request.urlopen("https://www.youtube.com/results?"+ query_string)

	results = re.findall(r"watch\?v=(\S{11})",formatUrl.read().decode())

	clip = requests.get("https://www.youtube.com/watch?v=" + "{}".format(results[0]))
	clip2 = "https://www.youtube.com/watch?v=" + "{} ".format(results[0])
	
	return clip2

@bot.event
async def on_ready():
    print(f'{bot.user} is connected to the following guild:\n')

@bot.command()
async def play(ctx,url):
	streamer = ytdl({'format_id':'audio-low','ext':'webm','vcodec':'none'})
	link =streamer.extract_info(url,download=False)["formats"][0]["url"]

	chann = ctx.author.voice.channel 
#
	client = await chann.connect(timeout=0.5)
	audio =  discord.FFmpegPCMAudio(link,args=["-vn","-acodec"])
	client.play(audio)
	


bot.run(TOKEN)


