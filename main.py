import discord
import re
from discord.ext import commands
from tinydb import TinyDB, Query

Inten = discord.Intents.all()
Eagle = commands.Bot(command_prefix='.',intents=Inten)


User = Query()
db   = TinyDB('db.json')

@Eagle.event
async def on_ready():
    print("Bot ready.")
    Eagle.User = Query()
    Eagle.db = TinyDB('vouches.json')

@Eagle.command(name="vouch")
async def vouch(context, args : discord.Member):

    Eagle.db.insert({'name': str(args.id), 'vouches' : 0,'vouchby':str(context.message.author.id)})

    await context.send("Vouched.")


@Eagle.command()
async def addvouch(context, args:discord.Member, args2: discord.Member):
		Eagle.db.insert({'name': str(args.id), 'vouches' : 0,'vouchby':str(args2.id)})
		await context.send("Vouched.")

	
@Eagle.command()
async def scrapevouches(context,tovouch:discord.Member = None):
	if tovouch == None:	
		tovouch = context.message.author
	vouchers = []
	async for message in context.channel.history(limit=200):
		vouchers.append(message.author.id)

	for vouch in vouchers:
		Eagle.db.insert({'name': str(tovouch.id), 'vouches' : 0,'vouchby':str(vouch)})
		print("Added Voucher")

@Eagle.command(name="rep")
async def rep(context, args : discord.Member):

    vouchesofuser = Eagle.db.search(Eagle.User.name == str(args.id))

    embed = discord.Embed(title="Vouches", description=str(args.id) + " has " + str(len(vouchesofuser)) + " vouches.", color=0x00ff39)
    await context.send(embed=embed)

@Eagle.command(name="vouches")
async def vouches(context, args : discord.Member = None):
		if args == None:
			args = context.message.author
			
		list_name = []
		result = Eagle.db.search(Eagle.User.name == str(args.id))

		for name in result:
				listtoappend = f"<@{name['vouchby']}>"
				list_name.append(listtoappend)

		embed = discord.Embed(title=f"Vouches of {str(args)}", description=', '.join(list_name ), color=0x00d9ff)
		await context.send(embed=embed)





Eagle.run("")
