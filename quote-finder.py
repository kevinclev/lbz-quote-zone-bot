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

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-------')

# handle CommandNotFound errors so that the output isn't ass blasted by this error.
# because likely there are other bots that use the ! as prefix
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass


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
    if '!' in name:
        msg_filter = '- ' + name
    else:
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

@quotes.error
async def quotes_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You must specify a user.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Not a valid user")

bot.run(discord_token)