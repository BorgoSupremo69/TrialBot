import disnake
from disnake.ext import commands
import re
class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="ban an user")
    @commands.has_permissions(ban_members=True)
    async def ban(self, inter, member:disnake.Member=commands.Param(description="Utente da bannare"), delete_days=commands.Param(default=0, description="delete days time", min_length=0, max_length=1), reason:str=commands.Param(description="reason per il ban")):
        if int(delete_days):
            if str(reason):
                await member.ban(delete_message_days=delete_days, reason=reason)
                await inter.send(embed=disnake.Embed(
                    title="banned user",
                    description=f"{member.mention} è stato bannato per: {reason}."
                ))
            else:
                await inter.send('"reason" non è una stringa ma un numero, ad esempio rifai il comando così:"reason:spam".', ephemeral=True)
        else:
            await inter.send('"delete_days" dovrebbe essere un numero. ',ephemeral=True)
    @commands.slash_command(description="unban an user")
    @commands.has_permissions(ban_members=True)
    async def unban(self, inter, member:disnake.Member=commands.Param(description="Utente da sbannare"),  reason:str=commands.Param(description="reason per il ban")):
            
            if str(reason):
                await member.unban(reason=reason)
                await inter.send(embed=disnake.Embed(
                    title="unbanned user",
                    description=f"{member.mention} è stato sbannato per: {reason}."
                ))
            else:
                await inter.send('"reason" non è una stringa ma un numero, ad esempio rifai il comando così:"reason:spam".', ephemeral=True)

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, inter, member: disnake.Member, duration: str):
        time_regex = re.compile('^(\d+)([smhd])$')
        time_dict = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}

        match = time_regex.match(duration)
        if match is None:
            await inter.send('Invalid duration, Please use a valid duration format (e.g. 1d, 1h, 1m, 1s).')
            return

        duration = int(match.group(1)) * time_dict[match.group(2)]

        await member.timeout(duration=float(duration))
        await inter.send(f'{member.mention} time out per {duration} secondi.')


    @commands.slash_command(description="kick an user")
    @commands.has_permissions(kick_members=True)
    async def kick(self, inter, member: disnake.Member = commands.Param(description="Utente da kickare"), reason: str = commands.Param(description="reason per il kick")):
        if str(reason):
            await member.kick(reason=reason)
            await inter.send(embed=disnake.Embed(
                title="kicked user",
                description=f"{member.mention} è stato kickato per: {reason}."
            ))
        else:
            await inter.send('"reason" non è una stringa ma un numero, ad esempio rifai il comando così:"reason:spam".', ephemeral=True)

def setup(bot):
    bot.add_cog(moderation(bot))