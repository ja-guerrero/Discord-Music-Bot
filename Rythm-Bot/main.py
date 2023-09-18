import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
import yt_dlp
load_dotenv()



FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}


class Bot:
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        self.bot = commands.Bot(command_prefix="!", intents=intents)
        self.Token = os.getenv("DISCORD_TOKEN")

        self.que =[]
       
        self.methods()
        self.bot.run(self.Token)



        
    def get_src(self,url):
        ydl_opts = {
            'format': 'm4a/bestaudio/best',
            # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
            'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url = ydl.sanitize_info(info)["formats"][5]["url"]
            title =  ydl.sanitize_info(info)["title"]   
        print(url,title)
        return([url, title])


    def type(self,url):
        if "spotify" in url.lower():
            return "Spotify"
        if "youtube" in url.lower():
            return "youtube"

    def isPlaylist(url):
        pass

    def play_next(self,ctx, source):
        vc = ctx.message.guild.voice_client
        try:
            if len(self.que) >= 1:
            
                self.que.pop(0)		
                vc.play(discord.FFmpegPCMAudio(source=source[0], **FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx,self.que[0]))

            else:             
                ctx.message.channel.send("End of Que")
                asyncio.sleep(90)
                if not vc.is_playing():
                    vc.disconnect()    
        except:
            ctx.message.channel.send("End of Que")
            asyncio.sleep(90)
            if not vc.is_playing():
                vc.disconnect(ctx)


    def show_que(self):
        message = ""
        for i in range(len(self.que)):
            message += f"{i}. {self.que[i][1]} \n"
        return message

    def methods(self):



        @self.bot.command()
        async def play(ctx,url):
            
            
            #if self.type(url) == "spotify":
            #    audio = Spotify_API(url)
        
            audio = self.get_src(url)
            self.que.append(audio)

            if len(self.que)>=1:
                await ctx.message.channel.send(f"Added to que: {url} ")
                await ctx.message.channel.send(self.show_que())

            chann = ctx.author.voice.channel
            client = ctx.message.guild.voice_client

            if client == None:
                client = await chann.connect(timeout=1)
                print(f"new-Client: {client}")
                self.que.clear()
            
            if not client.is_playing():
                client.play(discord.FFmpegPCMAudio(source=audio[0], **FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx=ctx,source=audio)) 



        @self.bot.command()
        async def fs(ctx):
            client = ctx.message.guild.voice_client
            if client.is_playing():
                client.stop()


        @self.bot.command()
        async def pause(ctx):
            server = ctx.message.guild
            client = server.voice_client
            if client.is_playing():
                client.pause()
            else:
                ctx.message.channel.send("There is Nothing to pause you Dumb Fuck")



        @self.bot.command()
        async def resume(ctx):
            server = ctx.message.guild
            client = server.voice_client
            if client.is_paused():
                client.resume()
                ctx.message.channel.send(f"{self.que[0]} has been resumed")
            else:
                ctx.message.channel.send("There is Nothing to resume you Dumb Fuck")


if __name__ == '__main__':
    Bot()






