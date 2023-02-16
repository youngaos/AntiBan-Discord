import discord, os
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=".", intents=intents)
bot.remove_command('help')
token = os.getenv("token")

channels = [1067567082465665135]
allowed_mentions = discord.AllowedMentions(everyone=False,roles=False,users=True)

@bot.event
async def on_ready():
  print(f'Logged in; {bot.user} ')
  global startTime
  await bot.change_presence(activity=discord.Streaming(
    name='.gg/deaddestroyers', url='https://www.twitch.tv/1.'))

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id not in channels:
        webhook = None
        webhooks = await message.channel.webhooks()
        if len(webhooks) > 0:
            webhook = webhooks[0]

        if webhook is None:
            webhook = await message.channel.create_webhook(name='Random')
        content = message.content
        avatar_url = message.author.display_avatar
        if message.attachments:
            attachment = message.attachments[0]
            filename = attachment.filename
            await attachment.save(filename)
            with open(filename, "rb") as f:
                picture = discord.File(f)
                await message.delete()
                await webhook.send(file=picture, content=content, username=message.author.name, avatar_url=avatar_url, allowed_mentions=allowed_mentions)
            os.remove(filename)
        else:
            await message.delete()
            await webhook.send(content, username=message.author.name, avatar_url=avatar_url, allowed_mentions=allowed_mentions)
    await bot.process_commands(message)

keep_alive()
bot.run(token)
