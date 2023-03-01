import disnake
from disnake.ext import commands
import os
import json
from disnake.ext import tasks
import random
from datetime import datetime
import aiosqlite
from cogs.cogLoader import cogLoader
#imports

#open config file and set up the bot

with open("config.json") as configFile:
    config = json.load(configFile)

token = config["token"]
prefix = config["prefix"]


#bot declaration

intents=disnake.Intents.all() #bot intents
bot = commands.Bot(command_prefix=prefix, intents=intents,owner_id=[1022620526314786817, 759006167291658280])
bot.loaded_cogs = []
bot.unloaded_cogs = []






    #register a command to check the status of cogs
    
        
@commands.is_owner()
@bot.command()
async def cogs_status(ctx):
    
    cog_list = commands.Paginator(prefix='', suffix='')
    cog_list.add_line('**✅ Successfully Loaded:**')
    for cog in bot.loaded_cogs:
            cog_list.add_line('- ' + cog)
            cog_list.add_line('**❌ Not Loaded:**')
    for cog in bot.unloaded_cogs:
            cog_list.add_line('-' + cog)
        
    for page in cog_list.pages:
                await ctx.send(page)
    #tasks to change status every precise amount of time
@tasks.loop(minutes=1.0)
async def statusChanger() -> None:
    statuses = config["statuses"]
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.playing, name=f"{random.choice(statuses)}"))


    #listener for when the bot is ready
@bot.listen("on_ready")
async def clientOnReadyListener():
    current_time =datetime.now.strftime("%Y-%m-%d %H:%M:%S")
    cogLoader.checkDirs()
    cogLoader.autoLoadCogs()
    cogLoader.registerUnloadedCogs()
    statusChanger.start()
    print(f"{current_time} Bot up and running ")




if __name__ == '__main__':
    bot.run(token)