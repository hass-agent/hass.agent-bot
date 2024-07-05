import nextcord
from nextcord.ext import commands
from nextcord import Interaction, Message

HELP_CHANNEL_ID = 1173034142603165756
tag_select_options = [
    nextcord.SelectOption(
        label="App Issue",
        value=1183576104255115405,
        emoji=nextcord.PartialEmoji(name="HASSAgentLogo", id=1173119197329506355),
    ),
    nextcord.SelectOption(
        label="Setup | Question", value=1173036123208024177, emoji="⚙️"
    ),
    nextcord.SelectOption(label="HA Issue", value=1173088649034858526, emoji="📦"),
    nextcord.SelectOption(label="Documentation", value=1173036162110206062, emoji="📑"),
]


class ThreadTitle(nextcord.ui.TextInput):
    def __init__(self):
        super().__init__(
            label="Enter New Thread Title", placeholder="E.g Problem creating command"
        )


class MoveThreadModal(nextcord.ui.Modal):
    def __init__(self, channel, message, selected_tags):
        super().__init__(title="Move message")

        self.channel = channel
        self.message = message
        self.selected_tags = selected_tags

        self.thread_title = ThreadTitle()
        self.add_item(self.thread_title)

    async def callback(self, interaction: Interaction):
        tags = []
        for id in self.selected_tags:
            tags.append(nextcord.ForumTag(id=id, name=None))

        await self.channel.create_thread(
            name=self.thread_title.value,
            content=self.message,
            applied_tags=tags,
        )


class TagSelect(nextcord.ui.Select):
    def __init__(self, channel, message):
        super().__init__(
            placeholder="Select Tags", options=tag_select_options, max_values=4
        )

        self.channel = channel
        self.message = message

    async def callback(self, interaction: Interaction):
        await interaction.response.send_modal(
            MoveThreadModal(self.channel, self.message, self.values)
        )


class MoveThreadView(nextcord.ui.View):
    def __init__(self, channel, message):
        super().__init__()

        self.add_item(TagSelect(channel=channel, message=message))


class MessageManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.message_command(name="Move to Get Help")
    async def move_to_get_help(self, interaction: Interaction, message: Message):
        # Check if the user CAN'T manage threads
        if not interaction.user.guild_permissions.manage_threads:
            # Check if the message is NOT a users own
            if not interaction.user == message.author:
                await interaction.response.send_message(
                    "You don't have permission to move messages.", ephemeral=True
                )
                return

        # Send the view with the select menu to the user
        view = MoveThreadView(
            channel=self.bot.get_channel(HELP_CHANNEL_ID), message=message.content
        )
        await interaction.response.send_message(
            "Select tags for the new thread:", view=view, ephemeral=True
        )


def setup(bot):
    bot.add_cog(MessageManagementCog(bot))
