import os
import discord

from discord.ext import commands

# Discord api token for bot
discord_token = os.environ.get('DISCORD_TOKEN')
# Channel ID for Quote Zone
channel_id = os.environ.get('QZONE_ID')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!')

@bot.command(name="version", description="Shows the version of the bot.")
async def version(ctx):
    await ctx.send("beta af, don't get mad if I mess something up")

# Command: !quotes @user
# Description: Pulls all the quotes from the quote-zone for the specified user and post them in the current channel
@bot.command(name="quotes", description="Pulls all quotes for the specified user")
async def quotes(ctx, member: discord.Member):
    channel = bot.get_channel(int(channel_id))
    messages = await channel.history(limit=2000).flatten()
    name = member.mention
    
    # discord.py does this weird thing where mentions in a message insert a ! before the user id
    # where as the Member class does not do this so I had to insert it myself so that the filter would work
    # filter basically looks for the user being quoted since our format always is "- @user" for someone being
    # quoted
    msg_filter = '- ' + name[:2] + '!' + name[2:]
    quotes = []

    for msg in messages:
        if msg_filter in msg.content:
            # removes the mention so they dont get @'ed to hell
            quote = msg.content.replace(msg_filter, '')
            quotes.append(quote)
    
    if not quotes:
        await ctx.send("User does not have any quotes. Which means that they do not have any server impact.")
    else:
        await ctx.send("\n".join(quotes))


bot.run(discord_token)