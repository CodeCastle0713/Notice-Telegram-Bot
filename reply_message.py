from telethon import TelegramClient, events

# Replace with your values
api_id = '25015625'
api_hash = 'd52af4fc5ca7de659b0962521f25a7c3'

# Create the client and connect
client = TelegramClient('bot', api_id, api_hash).start()

@client.on(events.NewMessage(pattern='/hello'))
async def hello(event):
    await event.reply('Hello!')

# Start the bot
print("Bot is running...")
client.run_until_disconnected()