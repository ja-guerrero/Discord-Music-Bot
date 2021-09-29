import os
import asyncio 
import discord
#from dotenv import load_dotenv
from discord.ext import commands
import re,requests,subprocess,urllib.parse,urllib.request
from bs4 import BeautifulSoup
import pafy
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}




#load_dotenv()

#TOKEN = os.getenv('ODkxODAwMTE2OTgwMjI4MTU2.YVDnlA.WPnq8XkOjalTwtFQHmKI2fFzNhk')
TOKEN = "ODkxODAwMTE2OTgwMjI4MTU2.YVDnlA.WPnq8XkOjalTwtFQHmKI2fFzNhk"

bot = commands.Bot(command_prefix='!') 

que = []

def get_audio(name):

	query_string = urllib.parse.urlencode({"search_query":name})

	formatUrl = urllib.request.urlopen("https://www.youtube.com/results?"+ query_string)

	results = re.findall(r"watch\?v=(\S{11})",formatUrl.read().decode())

	clip = requests.get("https://www.youtube.com/watch?v=" + "{}".format(results[0]))
	clip2 = "https://www.youtube.com/watch?v=" + "{} ".format(results[0])
	
	return clip2

def play_next(ctx, source):
    if len(que) >= 1:
        que.remove(que[0])
        vc = ctx.message.guild.voice_client
        vc.play(discord.FFmpegPCMAudio(source=source), after=lambda e: play_next(ctx,que[0]))
        asyncio.run_coroutine_threadsafe(vc.disconnect(ctx), self.bot.loop)
        asyncio.run_coroutine_threadsafe(ctx.send("No more songs in queue."))

@bot.event
async def on_ready():
    print(f'{bot.user} is connected to the following guild:\n')

@bot.command()
async def play(ctx,url):

	chann = ctx.author.voice.channel 
	client = ctx.message.guild.voice_client
	if client == None:
		client = await chann.connect(timeout=1) 
		
	
	song = pafy.new(url)

	source = song.getbestaudio()

	que.append(source.url)


	if not client.is_playing():
		client.play(discord.FFmpegPCMAudio(source=source.url), after=lambda e: play_next(ctx,url))
	

@bot.command()
async def pause(ctx):
	server = ctx.message.guild
	audio = server.voice_client
	audio.pause()



bot.run(TOKEN)


