import os
import time
from asyncio import sleep
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

intents = discord.Intents.default()
intents.members = True

amongus = pafy.new("https://www.youtube.com/watch?v=4KfC923EFsY")
audio = amongus.getbestaudio()
sound = audio.url


drip_theme = pafy.new("https://www.youtube.com/watch?v=grd-K33tOSM")
drip_theme =drip_theme.getbestaudio()
drip_theme =drip_theme.url


bot = commands.Bot(command_prefix='!', intents=intents) 

que = []

def show_que():
	message = ""
	for i in range(len(que)):
		message += f"{i}. {que[i].title} \n"
	return message

def get_url(name):

	query_string = urllib.parse.urlencode({"search_query":name})

	formatUrl = urllib.request.urlopen("https://www.youtube.com/results?"+ query_string)

	results = re.findall(r"watch\?v=(\S{11})",formatUrl.read().decode())

	clip2 = "https://www.youtube.com/watch?v=" + "{} ".format(results[0])
	
	return clip2



def play_next(ctx, source):
	
	if len(que) >= 1:
		que.remove(que[0])		
		vc = ctx.message.guild.voice_client
		
		print(que)
		vc.play(discord.FFmpegPCMAudio(source=source, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx,que[0].url))
	else:
		asyncio.sleep(90) #wait 1 minute and 30 seconds
		if not vc.is_playing():
			disconnect(ctx)



@bot.event
async def on_ready():
    print(f'{bot.user} is connected to the following guild:\n')
    guilds = await bot.fetch_guilds(limit=150).flatten()
    guild = bot.get_guild(431948594023759874)
    print(guilds)
    member = guild.get_member(642375047411007519)
    await member.edit(nick="IM A FAGGOT")


@bot.command()
async def restart(ctx):
	client = ctx.message.guild.voice_client
	if client.is_playing():
		client.stop()
	que.insert(0,que[0])


@bot.command()
async def play(ctx,url):

	chann = ctx.author.voice.channel

	client = ctx.message.guild.voice_client

	print(f"Client: {client}")


	if client == None:

		client = await chann.connect(timeout=1)

		print(f"new-Client: {client}")

		que.clear()


	
	song = pafy.new(url)

	source = song.getbestaudio()
	print(source)
	
	que.append(source)

	if len(que)>1:
		await ctx.message.channel.send(f"Added to que: {source.title} ")
		await ctx.message.channel.send(show_que())


	print(que)
	
	if not client.is_playing():
		client.play(discord.FFmpegPCMAudio(source=source.url, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx,url))


	

@bot.command()
async def pause(ctx):
	server = ctx.message.guild
	client = server.voice_client
	if client.is_playing():
		client.pause()
		ctx.message.channel.send(f"{url[0].name} has been Paused")
	else:
		ctx.message.channel.send("There is Nothing to pause you Dumb Fuck")


async def resume(ctx):
	server = ctx.message.guild
	client = server.voice_client
	if client.is_paused():
		client.resume()
		ctx.message.channel.send(f"{url[0].name} has been resumed")
	else:
		ctx.message.channel.send("There is Nothing to resume you Dumb Fuck")





@bot.command()
async def fs(ctx):
	client = ctx.message.guild.voice_client
	if client.is_playing():
		client.stop()








@bot.command()
async def sus(ctx):
	chann = ctx.author.voice.channel 
	client = ctx.message.guild.voice_client
	if client == None:
		client = await chann.connect()
	client.play(discord.FFmpegPCMAudio(sound))
	time.sleep(2)
	await client.disconnect()





@bot.command()
async def amogus(ctx):
	chann = ctx.author.voice.channel 
	client = ctx.message.guild.voice_client
	if client == None:
		client = await chann.connect(timeout=2)

	if client.is_playing():
		client.stop()

	client.play(discord.FFmpegPCMAudio(drip_theme,**FFMPEG_OPTIONS))
	while client.is_playing():
		await sleep(1)
	await client.disconnect()






@bot.command()
async def kc(ctx): 
	cody = ctx.guild.get_member(716894553633980447)
# members is now a list of Member...
	await cody.edit(voice_channel=None)










@bot.event
async def on_member_update(before, after):
    if before.id == 642375047411007519:
        if str(after.nick) != "IM A  FAGGOT":
            # also would be able to get the guild via after.guild or before.guild
            guild = bot.get_guild(431948594023759874)
            member = guild.get_member(after.id)
            await member.edit(nick="IM A FAGGOT")



bot.run(TOKEN)


