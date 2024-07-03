import nextcord
from nextcord import Interaction
from nextcord.ext import commands

class HelpMonitorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.monitor_channels = [1173033285845266515]  # Replace with the actual channel IDs to monitor
        self.excluded_users = [1192941827167371314]  # Replace with the actual user IDs to exclude
        self.reaction_logs = {}  # Dictionary to store reaction counts

    @commands.Cog.listener()
    async def on_message(self, message):
        # Check if the message is in one of the monitored channels
        if message.channel.id in self.monitor_channels:
            # Check if the message is not from an excluded user
            if message.author.id not in self.excluded_users:
                # Check if the message contains keywords indicating the user needs help
                for keyword in ["help", "issue", "problem"]:
                    if keyword.lower() in message.content.lower():
                        # Create an embed for the response
                        embed = nextcord.Embed(
                            title="Channel Monitor Bot",
                            description=f"Hey {message.author.mention},\n\nIt looks like you might need help! Please head over to the help channel so that discussion is organized and we can get answers quicker!\n\n**<#1173034142603165756>**",
                            color=0x42bdf5  # Replace with the desired color code
                        )
                        embed.set_footer(text=f"Keyword used: {keyword}\n\nReact thumbs down to this message if I was wrong.")

                        # Send the embed as a response
                        await message.channel.send(embed=embed)
                        break  # Stop checking keywords after the first match

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # Check if the reaction is a thumbs-down emoji and the user is not a bot
        if str(reaction.emoji) == "👎" and not user.bot:
            # Log the thumbs-down reaction for later analysis
            self.log_reaction_info(reaction.message.id, reaction.message.created_at)


    def log_reaction_info(self, message_id, timestamp):
        # Log the message ID, timestamp, and update the reaction count
        if message_id not in self.reaction_logs:
            self.reaction_logs[message_id] = {"count": 1, "timestamp": timestamp}
        else:
            self.reaction_logs[message_id]["count"] += 1

        print(f"Thumbs-Down Reactions for Message ID {message_id}: {self.reaction_logs[message_id]['count']}")

        # Limit the logs to the most recent 10 items
        if len(self.reaction_logs) > 10:
            oldest_message_id = min(self.reaction_logs, key=lambda x: self.reaction_logs[x]["timestamp"])
            del self.reaction_logs[oldest_message_id]
            print(f"Removed oldest message ID: {oldest_message_id}")

    @nextcord.slash_command(name="get-monitor-logs", description="Shows list of messages with thumbs down", guild_ids=[1173033284519862392])
    async def get_reaction_logs(self, interaction: Interaction):
        # Command to get the current thumbs-down reaction logs
        user_id = interaction.user.display_name
        
        # Create an embed for the response
        embed = nextcord.Embed(
            title="Thumbs-Down Reaction Logs",
            description=f"Here are the thumbs-down reaction logs for messages in the monitored channel.",
            color=0x42bdf5  # Replace with the desired color code
        )

        # Add a field for each log entry
        for message_id, data in self.reaction_logs.items():
            timestamp = data["timestamp"].strftime("%H:%M %d/%m")
            count = data["count"]
            field_value = f"[{user_id}](https://discord.com/channels/{interaction.guild.id}/{self.monitor_channels[0]}/{message_id}) - Thumbs-Down Count: {count}"
            embed.add_field(name=f"Timestamp: {timestamp}", value=field_value, inline=False)

        # Send the embed as a response, visible only to the user who triggered the command
        await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(HelpMonitorCog(bot))
