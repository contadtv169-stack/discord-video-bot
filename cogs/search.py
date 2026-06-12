import discord
from discord.ext import commands
from discord import app_commands
from utils.downloader import search_all

class Search(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="buscar", description="Busca vídeos no YouTube, TikTok e Kwai")
    @app_commands.describe(query="Termo de busca", max_results="Quantidade de resultados (max 5)")
    async def buscar(self, interaction: discord.Interaction, query: str, max_results: int = 3):
        await interaction.response.defer()
        max_results = min(max_results, 5)

        results = await search_all(query, max_results)

        if not results:
            await interaction.followup.send("Nenhum vídeo encontrado.")
            return

        embed = discord.Embed(
            title=f"Resultados para: {query}",
            color=discord.Color.blue()
        )

        for i, video in enumerate(results, 1):
            platform_emoji = {
                "youtube": "▶️",
                "tiktok": "🎵",
                "kwai": "📱",
            }.get(video["platform"], "🎬")
            embed.add_field(
                name=f"{platform_emoji} #{i} - {video['title'][:80]}",
                value=f"**Plataforma:** {video['platform'].capitalize()}\n"
                      f"**Link:** {video['url']}\n"
                      f"**Canal:** {video['channel']}",
                inline=False
            )

        embed.set_footer(text="Use !baixar <url> para baixar um vídeo")
        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Search(bot))
