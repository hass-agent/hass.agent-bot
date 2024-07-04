import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import re


class HelpMonitorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.monitor_channels = [1173033285845266515]
        self.excluded_users = [638245963240046592, 135056992745029632]
        self.last_reminder_message = None

    @commands.Cog.listener()
    async def on_message(self, message):
        # Check if the message is in one of the monitored channels and not from an excluded user
        if (
            message.channel.id in self.monitor_channels
            and message.author.id not in self.excluded_users
        ):
            # Use regular expression to check for the whole word "help"
            if re.search(r"\b(help|issue|problem)\b", message.content, re.IGNORECASE):
                # Delete the last reminder message if it exists
                if self.last_reminder_message:
                    try:
                        await self.last_reminder_message.delete()
                    except nextcord.NotFound:
                        pass  # The message was already deleted

                # Create an embed for the response
                embed = nextcord.Embed(
                    title="Channel Monitor Bot",
                    description=f"Hey {message.author.mention},\n\nIt looks like you might need help! Please head over to the help channel so that discussion is organized and we can get answers quicker!\n\n**<#1173034142603165756>**",
                    color=0x42BDF5,
                )

                # Send the embed as a response and store the message
                self.last_reminder_message = await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(HelpMonitorCog(bot))
