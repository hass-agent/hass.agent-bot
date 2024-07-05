import nextcord
from nextcord import Interaction, Embed
from nextcord.ext import commands
import time


class DetailsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="bug_details",
        description="Show message with details needed for a bug",
        guild_ids=[1173033284519862392],
    )
    async def bugdetails(self, interaction: Interaction):
        embed = Embed(
            color=0x42BDF5,
            title="Bug Report Details",
            description="Please provide us with all of the below details so we can best help you solve this issue.\n\n### Version Number\nVersion of the app can be found under `? -> Beneath Logo`\n\n### Extended logs\nUnder `Configuration -> Logging` of the app you can enable extended logs and open the log folder. **Upload the most recent logs**",
        )
        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(DetailsCog(bot))
