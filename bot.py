import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import yt_dlp
import asyncio

# Load environment variables
load_dotenv()

# Configure yt-dlp
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': True,
    'no_warnings': True,
}

# Create bot with command prefix
bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

# Dictionary to store queue for each server
music_queues = {}
current_playing = {}

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='join')
async def join(ctx):
    """Join the voice channel"""
    if ctx.author.voice is None:
        await ctx.send("❌ You need to be in a voice channel!")
        return
    
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()
    await ctx.send(f"✅ Joined {voice_channel.name}")

@bot.command(name='leave')
async def leave(ctx):
    """Leave the voice channel"""
    if ctx.voice_client is None:
        await ctx.send("❌ Not connected to a voice channel!")
        return
    
    await ctx.voice_client.disconnect()
    await ctx.send("✅ Left the voice channel")

@bot.command(name='play')
async def play(ctx, *, url):
    """Play a YouTube video from URL"""
    if ctx.voice_client is None:
        if ctx.author.voice is None:
            await ctx.send("❌ You need to be in a voice channel!")
            return
        voice_channel = ctx.author.voice.channel
        vc = await voice_channel.connect()
    else:
        vc = ctx.voice_client
    
    # Add to queue
    guild_id = ctx.guild.id
    if guild_id not in music_queues:
        music_queues[guild_id] = []
    
    music_queues[guild_id].append(url)
    await ctx.send(f"✅ Added to queue: {url}")
    
    # Play if nothing is playing
    if not vc.is_playing():
        await play_next(ctx, vc, guild_id)

async def play_next(ctx, vc, guild_id):
    """Play the next song in queue"""
    if guild_id not in music_queues or len(music_queues[guild_id]) == 0:
        return
    
    url = music_queues[guild_id].pop(0)
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await ctx.send(f"🎵 Now playing: {url}")
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']
        
        source = discord.FFmpegPCMAudio(audio_url)
        vc.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(
            play_next(ctx, vc, guild_id), bot.loop
        ).result())
    except Exception as e:
        await ctx.send(f"❌ Error playing audio: {str(e)}")
        # Try next song in queue
        await play_next(ctx, vc, guild_id)

@bot.command(name='stop')
async def stop(ctx):
    """Stop the music"""
    if ctx.voice_client is None:
        await ctx.send("❌ Not connected to a voice channel!")
        return
    
    ctx.voice_client.stop()
    guild_id = ctx.guild.id
    if guild_id in music_queues:
        music_queues[guild_id] = []
    await ctx.send("⏹️ Stopped playing")

@bot.command(name='skip')
async def skip(ctx):
    """Skip the current song"""
    if ctx.voice_client is None or not ctx.voice_client.is_playing():
        await ctx.send("❌ Nothing is playing!")
        return
    
    ctx.voice_client.stop()
    await ctx.send("⏭️ Skipped to next song")

@bot.command(name='queue')
async def queue_cmd(ctx):
    """Show the music queue"""
    guild_id = ctx.guild.id
    if guild_id not in music_queues or len(music_queues[guild_id]) == 0:
        await ctx.send("📭 Queue is empty")
        return
    
    queue_list = "\n".join([f"{i+1}. {url}" for i, url in enumerate(music_queues[guild_id])])
    await ctx.send(f"📋 **Queue:**\n{queue_list}")

@bot.command(name='help')
async def help_command(ctx):
    """List all available commands"""
    help_text = """
    **🎵 Music Commands:**
    `!play <url>` - Play a YouTube video
    `!join` - Join your voice channel
    `!leave` - Leave the voice channel
    `!stop` - Stop the music
    `!skip` - Skip to next song
    `!queue` - Show the music queue
    `!help` - Show this message
    """
    await ctx.send(help_text)

# Run the bot
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)
