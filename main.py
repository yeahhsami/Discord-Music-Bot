import discord
from discord.ext import commands
from pytube import YouTube
import asyncio

intents = discord.Intents.default()
intents.voice_states = True
intents.messages = True
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print("The bot is ready for use! ")
    print('--------------------------')

@client.event
async def member_join(member):
    channel = client.get_channel(817094638879768669)
    await channel.send("Welcome!")
@client.event
async def member_remove(member):
    channel = client.get_channel(817094638879768669)
    await channel.send("Goodbye!")

# Command to join a voice channel
@client.command(pass_context= True)
async def join(ctx):
    if ctx.author.voice: #if user is running this command in voice channel
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.send(f"Joined voice channel: {channel.name}")
    else:
        await ctx.send("You are not connected to any voice channel.")

# Command to leave a voice channel
@client.command(pass_context = True)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the Voice Channel")
    else:
        await ctx.send("I am not in a voice Channel")



class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=1):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        yt = YouTube(url).streams.get_highest_resolution()
        filename = yt.download()
        return filename
# Command to play music from a YouTube URL

@client.command(name='play', help='To play a song')
async def play(ctx, url):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client

        # Check if the bot is connected to a voice channel
        if voice_channel is None:
            # Connect to a voice channel if not already connected
            voice_channel = await ctx.author.voice.channel.connect()

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=client.loop)

            # Check if the filename is a valid file path
            if filename:
                voice_channel.play(discord.FFmpegPCMAudio(executable="C:\\ffmpeg\\ffmpeg.exe", source=filename))
                await ctx.send('**Now playing:** {}'.format(filename))
            else:
                await ctx.send('Failed to get the audio file.')

    except Exception as e:
        await ctx.send("An error occurred: {}".format(str(e)))
@client.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")


@client.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

# Run the bot
client.run(BOTTOKEN)