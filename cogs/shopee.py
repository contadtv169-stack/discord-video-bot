import discord
from discord.ext import commands
from discord import app_commands
from utils.shopee import search_shopee_products, search_shopee_videos, get_product_info

class Shopee(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="shopee", description="Busca produtos/anúncios Shopee")
    @app_commands.describe(query="Nome do produto", max_results="Quantidade de resultados (max 5)")
    async def shopee(self, interaction: discord.Interaction, query: str, max_results: int = 3):
        await interaction.response.defer()
        max_results = min(max_results, 5)

        videos = await search_shopee_products(query, max_results)

        embed = discord.Embed(
            title=f"🛒 Shopee - {query}",
            description="Vídeos de produtos encontrados:",
            color=discord.Color.orange()
        )

        if videos:
            for i, v in enumerate(videos, 1):
                embed.add_field(
                    name=f"#{i} {v['title'][:80]}",
                    value=f"**Canal:** {v['channel']}\n**Link:** {v['url']}",
                    inline=False
                )
        else:
            embed.description = "Nenhum vídeo encontrado para este produto."

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="produto", description="Analisa um link de produto Shopee")
    @app_commands.describe(link="Link do produto Shopee")
    async def produto(self, interaction: discord.Interaction, link: str):
        await interaction.response.defer()

        info = await get_product_info(link)

        if not info:
            await interaction.followup.send(
                f"Não foi possível analisar o produto.\nLink: {link}"
            )
            return

        embed = discord.Embed(
            title="📦 Produto Shopee",
            color=discord.Color.green()
        )
        embed.add_field(name="Nome", value=info.get("title", "Desconhecido"), inline=False)
        embed.add_field(name="Preço", value=info.get("price", "Ver no site"), inline=True)
        embed.add_field(name="Link", value=link, inline=False)

        if info.get("thumbnail"):
            embed.set_thumbnail(url=info["thumbnail"])

        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Shopee(bot))
