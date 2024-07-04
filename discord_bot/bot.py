import os
from concurrent.futures import ThreadPoolExecutor
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from dotenv import load_dotenv

load_dotenv("../.env")

bot = commands.Bot(command_prefix="!", intents=nextcord.Intents.all())


@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user.name}")


@bot.slash_command(
    name="test", description="Test if bot is connected", guild_ids=[1173033284519862392]
)
async def test(interaction: Interaction):
    await interaction.response.send_message(
        "Bot is currently connected! :smile:", ephemeral=True
    )


bot.load_extension("get_help_cog")  # Load Get Help
bot.load_extension("help_monitor_cog")  # Load Help Monitor

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
