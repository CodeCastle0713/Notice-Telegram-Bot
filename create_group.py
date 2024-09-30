from telethon import TelegramClient, events, functions, types

# Replace with your values
api_id = '25015625'
api_hash = 'd52af4fc5ca7de659b0962521f25a7c3'

# Create the client and connect using bot token
client = TelegramClient('bot', api_id, api_hash).start()

async def create_channel_with_users(chname, descrip, usernames):
    # Create a new group (megagroup)
    result = await client(functions.channels.CreateChannelRequest(
        title=chname,
        about=descrip,
        megagroup=True  # Use megagroup=False if you want a channel instead of a group
    ))
    
    # Get the ID of the new group
    group_id = result.chats[0].id

    # Generate an invite link for the group
    invite_link = await client(functions.messages.ExportChatInviteRequest(
        peer=group_id
    ))

    # Convert the list of usernames to a list of user entities
    users = []
    for username in usernames:
        user = await client.get_entity(username)
        users.append(user)

    # Invite the users to the group
    await client(functions.channels.InviteToChannelRequest(
        channel=group_id,
        users=users
    ))

    await client(functions.channels.JoinChannelRequest(
        channel=group_id
    ))

    return {
        'group_id': group_id,
        'invite_link': invite_link.link
    }

@client.on(events.NewMessage(pattern='/click'))
async def click(event):
    sender = await event.get_sender()

    # Create a new group and get the invite link, including multiple users
    result = await create_channel_with_users(
        f'{sender.username} requested...', 
        'This is a new group created by bot', 
        ['keys811', 'mrssvetulek_wbbot']
    )

    # Send a response with the new group link
    await event.reply(
        f'Your group has been created! Click the link below to join:\n\n'
        f'🔗 [Join the Group]({result["invite_link"]})'
    )

@client.on(events.NewMessage(pattern='/custom (.*)'))
async def custom_command(event):
    username = event.pattern_match.group(1).strip() 
    group_id = '4513695471' 
    sender = await event.get_sender()
    hello_message = f'Hello, Chatter - @{sender.username} choose Model - {username}!'

    try:
        await client.send_message(int(group_id), hello_message)
        await event.reply(f'You choose {username} and message sent to the Boss!')
    except Exception as e:
        await event.reply(f'Error: {str(e)}')

# Start the bot
print("Bot is running...")
client.run_until_disconnected()