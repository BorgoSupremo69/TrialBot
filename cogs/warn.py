#si bruh, mi serve un altro cog per i warn 💀
import asyncio
import disnake
import aiosqlite
from disnake.ext import commands
import aiosqlite


class warn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_file = 'warnings.db'

    async def create_table_if_not_exists(self, conn):
        c = await conn.cursor()
        await c.execute('''CREATE TABLE IF NOT EXISTS warnings (user_id INTEGER PRIMARY KEY, warning_count INTEGER, reason TEXT)''')

    @commands.slash_command(description="Warna un utente per un motivo")
    @commands.has_permissions(moderate_members=True)
    async def warn(self, inter, user: disnake.User, *, reason: str):
        async with aiosqlite.connect(self.db_file) as conn:
            await self.create_table_if_not_exists(conn)
            c = await conn.cursor()
            await c.execute('''INSERT OR IGNORE INTO warnings (user_id, warning_count, reason) VALUES (?, 0, ?)''', (user.id, reason))
            await c.execute('''UPDATE warnings SET warning_count = warning_count + 1 WHERE user_id = ?''', (user.id,))
            await conn.commit()
            warning_count = await c.execute('''SELECT warning_count FROM warnings WHERE user_id = ?''', (user.id,))
            warning_count = await warning_count.fetchone()
            warning_count = warning_count[0]
            await inter.send(f'{user.mention} è stato warnato per: __**{reason}**__ \n Questo è il warn numero: {warning_count}')

    @commands.slash_command(description="mostra tutti i warn che un utente ha")
    @commands.has_permissions(moderate_members=True)
    async def warns(self, inter, user: disnake.User):
        async with aiosqlite.connect(self.db_file) as conn:
            await self.create_table_if_not_exists(conn)
            c = await conn.cursor()
            warns = await c.execute('''SELECT warning_count, reason FROM warnings WHERE user_id = ?''', (user.id,))
            warns = await warns.fetchall()
            if not warns:
                await inter.send(f'{user.mention} non ha warn, che bravo/a ragazzo/a!')
            else:
                output = f'Stats dei warn di {user.mention} :\n'
                for warn in warns:
                    output += f"Quantità di warn:  __**{warn[0]}**__, Motivo dell'ultimo warn:__**{warn[1]}**__\n"
                await inter.send(output)

    @commands.slash_command(description="rimuovi l'ultimo warn che ha ricevuto da un utente")
    @commands.has_permissions(moderate_members=True)
    async def unwarn(self, inter, user: disnake.User):
        async with aiosqlite.connect(self.db_file) as conn:
            await self.create_table_if_not_exists(conn)
            c = await conn.cursor()
            warns = await c.execute('''SELECT warning_count FROM warnings WHERE user_id = ?''', (user.id,))
            warns = await warns.fetchone()
            if not warns:
                await inter.send(f'{user.mention} non ha warn da togliere')
            else:
                warning_count = warns[0]
                if warning_count > 1:
                    await c.execute('''UPDATE warnings SET warning_count = warning_count - 1 WHERE user_id = ?''', (user.id,))
                else:
                    await c.execute('''DELETE FROM warnings WHERE user_id = ?''', (user.id,))
                await conn.commit()
                await inter.send(f'Tolto un warn da: {user.mention} ora ha __**{warning_count - 1}**__ warn')