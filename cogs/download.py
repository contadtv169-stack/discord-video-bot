import discord
from discord.ext import commands
from discord import app_commands
from utils.downloader import download_video, search_all
import os
import re

def extract_url(text: str) -> str | None:
    pattern = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
    match = re.search(pattern, text)
    return match.group(0) if match else None

class Download(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="baixar", description="Baixa um vídeo do YouTube, TikTok ou Kwai")
    @app_commands.describe(url="URL do vídeo para baixar")
    async def baixar(self, interaction: discord.Interaction, url: str):
        await interaction.response.defer()

        platform = "desconhecida"
        if "youtube" in url.lower() or "youtu.be" in url.lower():
            platform = "youtube"
        elif "tiktok" in url.lower():
            platform = "tiktok"
        elif "kwai" in url.lower():
            platform = "kwai"

        filepath = await download_video(url, platform)

        if filepath is None or not os.path.exists(filepath):
            await interaction.followup.send("Erro ao baixar o vídeo. Verifique a URL e tente novamente.")
            return

        filesize = os.path.getsize(filepath)
        if filesize > 25 * 1024 * 1024:
            await interaction.followup.send(
                f"O vídeo é muito grande para enviar pelo Discord (>25MB).\n"
                f"Link original: {url}"
            )
            os.remove(filepath)
            return

        filename = os.path.basename(filepath)
        try:
            with open(filepath, "rb") as f:
                file = discord.File(f, filename=filename)
                await interaction.followup.send(
                    content=f"✅ Vídeo baixado!\n**Link:** {url}",
                    file=file
                )
        except Exception as e:
            await interaction.followup.send(f"Erro ao enviar o vídeo: {e}")
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

    @commands.command(name="baixar")
    async def baixar_prefix(self, ctx: commands.Context, *, url: str):
        extracted = extract_url(url)
        if not extracted:
            await ctx.send("URL inválida. Envie um link válido do YouTube, TikTok ou Kwai.")
            return

        async with ctx.typing():
            platform = "desconhecida"
            if "youtube" in extracted.lower() or "youtu.be" in extracted.lower():
                platform = "youtube"
            elif "tiktok" in extracted.lower():
                platform = "tiktok"
            elif "kwai" in extracted.lower():
                platform = "kwai"

            filepath = await download_video(extracted, platform)

            if filepath is None or not os.path.exists(filepath):
                await ctx.send("Erro ao baixar o vídeo.")
                return

            filesize = os.path.getsize(filepath)
            if filesize > 25 * 1024 * 1024:
                await ctx.send(
                    f"O vídeo é muito grande para enviar pelo Discord (>25MB).\n"
                    f"Link original: {extracted}"
                )
                os.remove(filepath)
                return

            filename = os.path.basename(filepath)
            try:
                with open(filepath, "rb") as f:
                    file = discord.File(f, filename=filename)
                    await ctx.send(
                        content=f"✅ Vídeo baixado!\n**Link:** {extracted}",
                        file=file
                    )
            except Exception as e:
                await ctx.send(f"Erro ao enviar o vídeo: {e}")
            finally:
                if os.path.exists(filepath):
                    os.remove(filepath)

async def setup(bot: commands.Bot):
    await bot.add_cog(Download(bot))
