import os
os.system("pip install -r requirements.txt")
import discord
from discord.ext import commands
import colorama
from colorama import Fore
import json
from discord.ext.commands import has_permissions, MissingPermissions, CommandNotFound
from rsnchat import RsnChat
from dotenv import load_dotenv
load_dotenv()
def gclear():
    os.system('title Ai-Bot By @TheAxes&& cls' if os.name=='nt' else 'clear')

# don't remove credits else you gay

prefix = os.getenv('prefix')
token = os.getenv('token')
api_key = os.getenv('rsn_key')
activityname = os.getenv('activity_text')
rsn_chat = RsnChat(api_key)
ownerid = os.getenv('owner_id')
convos = []
banner_fuckyouifyouchangethis = f"""
{Fore.LIGHTCYAN_EX}
 ______  __ __    ___       ____  __ __    ___  _____
|      ||  |  |  /  _]     /    ||  |  |  /  _]/ ___/
|      ||  |  | /  [_     |  o  ||  |  | /  [_(   \_ 
|_|  |_||  _  ||    _]    |     ||_   _||    _]\__  |
  |  |  |  |  ||   [_     |  _  ||     ||   [_ /  \ |
  |  |  |  |  ||     |    |  |  ||  |  ||     |\    |
  |__|  |__|__||_____|    |__|__||__|__||_____| \___|
 {Fore.RESET}{Fore.RED}A AI Discord Bot Made By: @Theaxes {Fore.RESET}"""


client = commands.Bot(description='Ai-Bot', command_prefix=prefix, intents=
discord.Intents.all(), case_insensitive=True, help_command=None)



@client.event
async def on_ready():
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activityname))
	gclear()
	print(banner_fuckyouifyouchangethis)
	print(f"""{Fore.LIGHTYELLOW_EX}Connected : {Fore.BLUE}{client.user}{Fore.RESET}\n{Fore.LIGHTYELLOW_EX}Prefix : {Fore.BLUE}{prefix}""")
	
@client.event
async def on_message(message):
	await client.process_commands(message)
	if message.content.startswith(f'<@{client.user.id}>'):
		embed = discord.Embed(title=f"{client.user}", description = f"Hey, {message.author.mention}\n\nMy Prefix Is `{prefix}`\nUse `{prefix}help` To Get Started or `/help`")
		embed.set_footer(text="Made With ❤️ By TheAxes")
		await message.reply(embed=embed)
	if message.channel.id in convos:
		if message.author.bot:
			return
		else:
			gpt_response = rsn_chat.gpt(message.content)
			await message.reply(gpt_response.get('message', ''))
		
	

		
		
@client.hybrid_command(name="help", description="Shows Help Menu")
async def help(ctx):
	embed = discord.Embed(title="",
	description="help, askai, startconversation, imagine, stopconvo, ping, latest")
	await ctx.reply(embed=embed)
	
@client.hybrid_command(name="askai", description="Ask Anything From AI")
async def askai(ctx, *, query):
	msg = await ctx.reply("`generating response...`")
	try:
		gpt_response = rsn_chat.gpt(query)
		await msg.edit(content=gpt_response.get('message', ''))
	except Exception as e:
		await ctx.send(f"can't generate response: {e}")
	
	
@client.hybrid_command(name="startconversation", description="Start ChatBot in specific channel")
@has_permissions(administrator=True)
async def startconversation(ctx):
	msg = await ctx.reply(f"> Hello, Good To See You Have Interacted With Me <3, We Can Continue Talking Now in {ctx.channel.mention}, You Can `stop conversation` by sending `{prefix}stopconvo` in chat")
	convos.append(ctx.channel.id)
		
	
@client.hybrid_command(name="imagine", description="create image from your imagination")
async def imagine(ctx, *, query):
	msg = await ctx.reply("`generating response`")
	response = rsn_chat.dalle(query)
	await msg.edit(content=response["image"]["url"])
	
	
@client.hybrid_command(name="stopconvo", description="stop chatbot")
@has_permissions(administrator=True)
async def stopconvo(ctx):
	if ctx.channel.id in convos:
		convos.remove(ctx.channel.id)
		await ctx.reply("conversation has stopped")
	else:
		return
	
@client.hybrid_command(name='ping', description="Shows Bot Latency")
async def ping(ctx):
	await ctx.reply(embed=discord.Embed(title="", description=f"> *_Bot Latency_* : `{int(client.latency * 1000)}` ms\n"))
	
@client.hybrid_command(name="latest", description="Provides Latest Version")
async def latest(ctx):
	await ctx.reply(embed=discord.Embed(title="Made By @TheAxes", description=f"> *Current Version_* : `1.0`\n> Latest Version: [Click Here](https://github.com/TheAxes/Discord-AIChatBot/releases)"))
	
	

@client.hybrid_command(name="sync", description="sync slash commands")
async def sync(ctx):
    print("sync command")
    if ctx.author.id == int(ownerid):
        await client.tree.sync()
        await ctx.send('Command tree synced.')
    else:
        await ctx.send('You must be the owner')
	
client.run(token)

  
