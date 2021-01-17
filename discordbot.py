import discord
from discord.ext import commands
from random import randint
import names
import json

pickaxeTypes = ["Stone", "Copper", "Iron", "Steel", "Mithril", "Adamantite", "Obsidian"]
	
fishingRodTypes = ["Stone", "Copper", "Iron", "Steel", "Mithril", "Adamantite", "Obsidian"]

axeTypes = ["Stone", "Copper", "Iron", "Steel", "Mithril", "Adamantite", "Obsidian"]

bowTypes = ["Stone", "Copper", "Iron", "Steel", "Mithril", "Adamantite", "Obsidian"]

class Miner(object):
	"""docstring for Miner"""

	name = ""
	currentPickaxe = ""
	currentInventory = []

	def __init__(self):
		self.name = names.get_first_name()
		self.currentPickaxe = f"{pickaxeTypes[randint(0, (len(pickaxeTypes)-1))]} Pickaxe"
		self.currentInventory = []
		self.currentInventory.append(self.currentPickaxe)

class Fisherman(object):
	"""docstring for Fisherman"""

	name = ""
	currentFishingRod = ""
	currentInventory = []

	def __init__(self):
		self.name = names.get_first_name()
		self.currentFishingRod = f"{fishingRodTypes[randint(0, (len(fishingRodTypes)-1))]} Fishing Rod"
		self.currentInventory = []
		self.currentInventory.append(self.currentFishingRod)

class Woodcutter(object):
	"""docstring for Woodcutter"""

	name = ""
	currentAxe = ""
	currentInventory = []

	def __init__(self):
		self.name = names.get_first_name()
		self.currentAxe = f"{axeTypes[randint(0, (len(axeTypes)-1))]} Axe"
		self.currentInventory = []
		self.currentInventory.append(self.currentAxe)

class Hunter(object):
	"""docstring for Hunter"""

	name = ""
	currentBow = ""
	currentInventory = []

	def __init__(self):
		self.name = names.get_first_name()
		self.currentBow = f"{bowTypes[randint(0, (len(bowTypes)-1))]} Bow"
		self.currentInventory = []
		self.currentInventory.append(self.currentBow)

def class_to_dict(classObject):
	return (classObject.__dict__)

def list_to_json(listVar):
	dictVar = {}
	for x in range(len(listVar)):
		newD = {str(x):listVar[x].__dict__}
		dictVar = dictVar | newD
	return dictVar

def dict_to_list_of_miners(jsonDict):
	listVar = []
	for x in range(len(list(jsonDict.keys()))):
		foo = Miner()
		foo.name = jsonDict[str(x)]["name"]
		foo.currentPickaxe = jsonDict[str(x)]["currentPickaxe"]
		foo.currentInventory = jsonDict[str(x)]["currentInventory"]
		listVar.append(foo)
	return listVar

def dict_to_list_of_fishermen(jsonDict):
	listVar = []
	for x in range(len(list(jsonDict.keys()))):
		foo = Fisherman()
		foo.name = jsonDict[str(x)]["name"]
		foo.currentFishingRod = jsonDict[str(x)]["currentFishingRod"]
		foo.currentInventory = jsonDict[str(x)]["currentInventory"]
		listVar.append(foo)
	return listVar

def dict_to_list_of_woodcutters(jsonDict):
	listVar = []
	for x in range(len(list(jsonDict.keys()))):
		foo = Woodcutter()
		foo.name = jsonDict[str(x)]["name"]
		foo.currentAxe = jsonDict[str(x)]["currentAxe"]
		foo.currentInventory = jsonDict[str(x)]["currentInventory"]
		listVar.append(foo)
	return listVar

def dict_to_list_of_hunters(jsonDict):
	listVar = []
	for x in range(len(list(jsonDict.keys()))):
		foo = Hunter()
		foo.name = jsonDict[str(x)]["name"]
		foo.currentBow = jsonDict[str(x)]["currentBow"]
		foo.currentInventory = jsonDict[str(x)]["currentInventory"]
		listVar.append(foo)
	return listVar



client = commands.Bot(command_prefix = '.')
client.remove_command('help')

@client.event
async def on_ready():
	print('Bot is ready!')

@client.command(pass_context=True)
async def help(ctx):
	author = ctx.message.author
	embed = discord.Embed(title='List of Commands', description='Below are the commands you can use with the bot along with a description.', colour=discord.Colour.orange())
	embed.add_field(name='ping', value='Returns the ping value of you and the bot.', inline=False)
	embed.add_field(name='dice', value='Returns a random number between 1 and 6.', inline=False)
	embed.add_field(name='create/cr', value='Creates a specific type of human that you specify (miner/woodcutter/fisherman/hunter).', inline=False)
	embed.add_field(name='list/li', value='Lists every human that falls into the category you specify (humans/miners/woodcutters/fishermen/hunters).', inline=False)
	embed.add_field(name='inventory/inv', value="Lists all the items in the human's inventory (human's name).", inline=False)
	embed.add_field(name='mine', value='Makes every miner mine for ore.', inline=False)
	embed.add_field(name='fish', value='Makes every fisherman fish for fish.', inline=False)
	embed.add_field(name='woodcut', value='Makes every woodcutter cut trees to get wood.', inline=False)
	embed.add_field(name='hunt', value='Makes the hunters hunt for meat.', inline=False)
	await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
	await ctx.send(f'{round(client.latency * 1000)}ms')

@client.command(aliases=['roll'])
async def dice(ctx):
	await ctx.send(f'You rolled {randint(1, 6)}')

isTutorialOver = True #Should be changed to false when exporting the game.

file = open("data.json", "r")
jsonData = json.loads(file.read())

humans = []
miners = dict_to_list_of_miners(jsonData["miners"])
fishermen = dict_to_list_of_fishermen(jsonData["fishermen"])
woodcutters = dict_to_list_of_woodcutters(jsonData["woodcutters"])
hunters = dict_to_list_of_hunters(jsonData["hunters"])

def update_humans_list():
	for miner in miners:
		humans.append(miner)
	for fisherman in fishermen:
		humans.append(fisherman)
	for woodcutter in woodcutters:
		humans.append(woodcutter)
	for hunter in hunters:
		humans.append(hunter)

update_humans_list()

def update_data_json():
	updatedJsonData = {"miners": "", "fishermen": "", "woodcutters": "", "hunters": ""}

	updatedJsonData["miners"] = list_to_json(miners)
	updatedJsonData["fishermen"] = list_to_json(fishermen)
	updatedJsonData["woodcutters"] = list_to_json(woodcutters)
	updatedJsonData["hunters"] = list_to_json(hunters)

	dataJson = open("data.json", "w")
	dataJson.write(json.dumps(updatedJsonData, indent=4))
	dataJson.close()

@client.command(aliases=['cr'])
async def create(ctx, *, humanTypeToCreate):
	humanTypeToCreate = humanTypeToCreate.lower()
	if humanTypeToCreate == "miner":
		miner = Miner()
		humans.append(miner)
		miners.append(miner)
		embed = discord.Embed(title='Miner Creation Complete', description=f'{miner.name} the miner has just been born with a {miner.currentPickaxe}.', colour=discord.Colour.green())
		await ctx.send(embed=embed)
	elif humanTypeToCreate == "fisherman":
		fisherman = Fisherman()
		humans.append(fisherman)
		fishermen.append(fisherman)
		embed = discord.Embed(title='Fisherman Creation Complete', description=f'{fisherman.name} the fisherman has just been born with a {fisherman.currentFishingRod}.', colour=discord.Colour.green())
		await ctx.send(embed=embed)
	elif humanTypeToCreate == "woodcutter":
		woodcutter = Woodcutter()
		humans.append(woodcutter)
		woodcutters.append(woodcutter)
		embed = discord.Embed(title='Woodcutter Creation Complete', description=f'{woodcutter.name} the woodcutter has just been born with a {woodcutter.currentAxe}.', colour=discord.Colour.green())
		await ctx.send(embed=embed)
	elif humanTypeToCreate == "hunter":
		hunter = Hunter()
		humans.append(hunter)
		hunters.append(hunter)
		embed = discord.Embed(title='Hunter Creation Complete', description=f'{hunter.name} the hunter has just been born with a {hunter.currentBow}.', colour=discord.Colour.green())
		await ctx.send(embed=embed)
	else:
		embed = discord.Embed(title='Human Creation Failed', description="You didn't specify a valid human type.", colour=discord.Colour.dark_red())
		await ctx.send(embed=embed)
	update_data_json()

@client.command(aliases=['li'])
async def list(ctx, *, humanTypeToList):
	humanTypeToList = humanTypeToList.lower()
	if humanTypeToList == "humans":
		embed = discord.Embed(title='List of Humans', description='This is the list of humans.', colour=discord.Colour.blue())
		for human in humans:
			embed.add_field(name=human.name, value='HUMAN TYPE', inline=False)
		await ctx.send(embed=embed)
	elif humanTypeToList == "miners":
		embed = discord.Embed(title='List of Miners', description='This is the list of miners.', colour=discord.Colour.blue())
		for miner in miners:
			embed.add_field(name=miner.name, value=miner.currentPickaxe, inline=False)
		await ctx.send(embed=embed)
	elif humanTypeToList == "fishermen":
		embed = discord.Embed(title='List of Fishermen', description='This is the list of fishermen.', colour=discord.Colour.blue())
		for fisherman in fishermen:
			embed.add_field(name=fisherman.name, value=fisherman.currentFishingRod, inline=False)
		await ctx.send(embed=embed)
	elif humanTypeToList == "woodcutters":
		embed = discord.Embed(title='List of Woodcutters', description='This is the list of woodcutters.', colour=discord.Colour.blue())
		for woodcutter in woodcutters:
			embed.add_field(name=woodcutter.name, value=woodcutter.currentAxe, inline=False)
		await ctx.send(embed=embed)
	elif humanTypeToList == "hunters":
		embed = discord.Embed(title='List of Hunters', description='This is the list of hunters.', colour=discord.Colour.blue())
		for hunter in hunters:
			embed.add_field(name=hunter.name, value=hunter.currentBow, inline=False)
		await ctx.send(embed=embed)
	else:
		embed = discord.Embed(title='Human List Failed', description="You didn't specify a valid human type.", colour=discord.Colour.dark_red())
		await ctx.send(embed=embed)

@client.command(aliases=['inv'])
async def inventory(ctx, *, humanName):
	for human in humans:
		if human.name.lower() == humanName.lower():
			embed = discord.Embed(title=f"{human.name}'s Inventory", colour = discord.Colour.green())
			for item in human.currentInventory:
				embed.add_field(name=item, value='ITEM', inline=False)
			await ctx.send(embed=embed)

@client.command()
async def mine(ctx):
	embed = discord.Embed(title='Miners have finished mining!', colour = discord.Colour.red())

	if len(miners) < 1:
		embed = discord.Embed(title='There are no miners!', description="Use '.create miner' to make a miner.", colour = discord.Colour.dark_red())
		await ctx.send(embed=embed)
		return

	for miner in miners:
		miner.currentInventory.append("Ore")
		embed.add_field(name=miner.name, value='has received ore.', inline=False)

	await ctx.send(embed=embed)
	update_data_json()

@client.command()
async def fish(ctx):
	embed = discord.Embed(title='Fishermen have finished fishing!', colour = discord.Colour.red())

	if len(fishermen) < 1:
		embed = discord.Embed(title='There are no fishermen!', description="Use '.create fisherman' to make a fisherman.", colour = discord.Colour.dark_red())
		await ctx.send(embed=embed)
		return

	for fisherman in fishermen:
		fisherman.currentInventory.append("Fish")
		embed.add_field(name=fisherman.name, value='has received fish.', inline=False)

	await ctx.send(embed=embed)
	update_data_json()

@client.command()
async def woodcut(ctx):
	embed = discord.Embed(title='Woodcutters have finished woodcuting!', colour = discord.Colour.red())

	if len(woodcutters) < 1:
		embed = discord.Embed(title='There are no woodcutters!', description="Use '.create woodcutter' to make a woodcutter.", colour = discord.Colour.dark_red())
		await ctx.send(embed=embed)
		return

	for woodcutter in woodcutters:
		woodcutter.currentInventory.append("Wood")
		embed.add_field(name=woodcutter.name, value='has received wood.', inline=False)

	await ctx.send(embed=embed)
	update_data_json()

@client.command()
async def hunt(ctx):
	embed = discord.Embed(title='Hunters have finished hunting!', colour = discord.Colour.red())

	if len(hunters) < 1:
		embed = discord.Embed(title='There are no hunters!', description="Use '.create hunter' to make a hunter.", colour = discord.Colour.dark_red())
		await ctx.send(embed=embed)
		return

	for hunter in hunters:
		hunter.currentInventory.append("Meat")
		embed.add_field(name=hunter.name, value='has received meat.', inline=False)

	await ctx.send(embed=embed)
	update_data_json()

client.run('NzgyOTcxMDYyMDI3MTU3NTY1.X8T8oA.r9lbyUOVVAY2NJuizORVqGzUTr4')