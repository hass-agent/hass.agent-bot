import os
from concurrent.futures import ThreadPoolExecutor
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from dotenv import load_dotenv
from flask import Flask, request

import utils

load_dotenv()

bot = commands.Bot(command_prefix="!", intents=nextcord.Intents.all())
app = Flask(__name__)


@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user.name}")


@bot.slash_command(
    name="test", description="Test if bot is connected", guild_ids=[1173033284519862392]
)
async def test(interaction: Interaction):
    await interaction.response.send_message("Bot is currently connected! :smile:")


@app.route("/github-webhook", methods=["POST"])
def github_webhook():
    data = request.json
    message = utils.format_request_to_message(data)
    channel = bot.get_channel(1192948772888641566)
    channel.send(message)

    return "Webhook received successfully!", 200


bot.load_extension("get_help_cog")  # Load Get Help
bot.load_extension("help_monitor_cog")  # Load Help Monitor


def run_bot():
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))


def run_flask_app():
    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(run_bot)
        executor.submit(run_flask_app)
    while True:
        pass
