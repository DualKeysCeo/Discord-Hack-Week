import asyncio, discord, time, json, os, random

from requests import get 
from discord.ext import commands
from discord.ext.commands import Bot

start_time = time.time()
Client = discord.Client()
client = Bot(command_prefix="%", activity=discord.Game(name="Minecraft | %help"))

config = json.load(open("config.json", "r"))

@client.event
async def on_ready():
    """
    Executes when the bot loads
    """
    print(f"* Bot ready | {time.strftime('%H:%M:%S %A %B %d, %Y')}")

@client.command(pass_context=True)
async def mock(ctx):
    async for message in ctx.channel.history(limit=20):
        if message.id == ctx.channel.last_message_id:
            async for msg in ctx.channel.history(limit=20, before=message.created_at):
                content = msg.content.lower()
                mockedContent = ""
                for letter in content:
                    rand = random.randint(1,2)
                    if (rand == 1): letter = letter.upper()
                    mockedContent += letter
                await ctx.channel.send(mockedContent)
                return

@client.command(pass_context=True)
async def insult(ctx, user:discord.Member=None):
    if not user:
        user = ctx.message.author
    await ctx.trigger_typing()
    time.sleep(.5)
    insult = get("https://insult.mattbas.org/api/insult")
    await ctx.channel.send(f"{user.mention} {insult.text}")

@client.command(pass_context=True, brief="Says fuck you to someone", help="If you tag someone it tags them and says \"fuck you!\"")
async def fuck(ctx, user: discord.Member=None):
    await ctx.trigger_typing()
    time.sleep(.25)
    if user == ctx.message.author: await ctx.channel.send("Awww dont say that. :( You're a great person. Use this command on anyone tells you otherwise")
    if not user: user = ctx.message.author
    await ctx.channel.send(f"Hey, {user.mention}, fuck you!")

@client.command(pass_context=True, aliases=["cumpowder"], brief="Sends link to the \"AWW DUDE YOURE DRINKING CUM POWDER\" clip", help="Sends link to the \"AWW DUDE YOURE DRINKING CUM POWDER\" clip from Cody Ko")
async def cum(ctx):
    await ctx.channel.send(f"https://www.youtube.com/watch?v=3o8DPozNNNM")

@client.command(pass_context=True)
async def stop(ctx):
    if (ctx.author.id in config["devids"]):
        await client.logout()
        exit(1)
    else: await ctx.channel.send("Error")

client.run(config["token"])