import discord
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot logado como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Comandos slash sincronizados: {len(synced)}")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")

async def load_cogs():
    for cog in ["cogs.search", "cogs.download", "cogs.shopee"]:
        await bot.load_extension(cog)

if __name__ == "__main__":
    import asyncio
    asyncio.run(load_cogs())
    bot.run(TOKEN)
