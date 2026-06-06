# WarHero Discord Music Bot

A Discord bot that plays music from YouTube URLs.

## Setup

### 1. Install FFmpeg
**Windows:**
```bash
# Using chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get Your Bot Token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" tab and click "Add Bot"
4. Under the TOKEN section, click "Copy" to copy your bot token
5. Create a `.env` file in the project root and add:
```
DISCORD_TOKEN=your_bot_token_here
```

### 4. Invite Bot to Your Server
1. In Developer Portal, go to "OAuth2" > "URL Generator"
2. Select scopes: `bot`
3. Select permissions: `Send Messages`, `Read Messages/View Channels`, `Connect`, `Speak`
4. Copy the generated URL and open it in your browser
5. Select your server and authorize

### 5. Run the Bot
```bash
python bot.py
```

## Commands

- `!join` - Join your voice channel
- `!play <url>` - Play a YouTube video (e.g., `!play https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
- `!skip` - Skip to the next song in queue
- `!stop` - Stop playing and clear queue
- `!queue` - Show the current music queue
- `!leave` - Leave the voice channel
- `!help` - Show all commands

## Example Usage

```
!join
!play https://www.youtube.com/watch?v=dQw4w9WgXcQ
!queue
!skip
!stop
!leave
```

## Troubleshooting

**FFmpeg not found:** Make sure FFmpeg is installed and added to your PATH

**Bot won't connect:** Check that the bot has "Connect" and "Speak" permissions in your server

**No audio:** Make sure FFmpeg is properly installed

## Next Steps

You can enhance your bot by:
- Adding playlist support
- Adding volume control
- Adding now playing display
- Adding search functionality
