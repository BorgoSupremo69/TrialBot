import os
from main import bot

class cogLoader():

    #check if cogs folder exists
    def checkDirs() -> None:
        os.makedirs('cogs', exist_ok=True)


    #load cogs
    def autoLoadCogs() -> None:

        for file in os.listdir('cogs'):
            if file.endswith('.py') and os.path.isfile('cogs/{}'.format(file)) and file[:-3]:
                try:
                    bot.load_extension("cogs.{}".format(file[:-3]))
                    bot.loaded_cogs.append(file[:-3])
                except Exception as e:
                    print(e)
                else:
                    print('Succesfully loaded cog {}'.format(file))

    #tell what cogs didn't load
    def registerUnloadedCogs() -> None:
        for file in os.listdir('cogs'):
            if file.endswith('.py') and os.path.isfile('cogs/{}'.format(file)) and file[:-3] not in bot.loaded_cogs:
                bot.unloaded_cogs.append(file[:-3])