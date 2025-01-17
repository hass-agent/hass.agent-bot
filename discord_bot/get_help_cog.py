import asyncio
import nextcord
from nextcord.ext import commands

HELP_CHANNEL_ID = 1173034142603165756


class GetHelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        # Check if the thread is created in the specific target channel
        if thread.parent.id == HELP_CHANNEL_ID:
            # Retrieve and process tags from the thread
            tags = [tag.name.lower() for tag in thread.applied_tags]

            # Mark solution embed
            mark_solution_embed = nextcord.Embed(
                title="Help us Help Others!",
                description="To help others find answers, you can mark your question as solved via `Right click solution message -> Apps -> ✅ Mark Solution`",
                color=0x000000,
            )
            mark_solution_embed.set_image(url="attachment://mark_solution.png")

            # Tags embed
            tags_embed = nextcord.Embed(
                title="Help us Help You!",
                description="Please don't delete messages or posts because it makes it impossible to understand what happened. If you don't want your messages to be seen then don't post here.",
                color=0x000000,
            )

            users_to_ping = set()

            # Customize content based on tags
            if "app issue" in tags:
                users_to_ping.add(135056992745029632)
                tags_embed.description += "\n\n**Please provide us with the version number of your app.**\n> You can find it by clicking the ? at the bottom of the main page and checking under the logo that shows."

            if "ha issue" in tags:
                users_to_ping.add(638245963240046592)
                tags_embed.description += "\n\n**Please provide us with your integration version number.**\n> You can find it in `HACS -> HASS.Agent 2 -> Top left` for installed version number."

            if "documentation" in tags:
                users_to_ping.add(638245963240046592)
                tags_embed.description += "\n\n**Please provide us with a direct link to the documentation.**\n> Please use permalinks to the section in the docs you are referencing. A guide for this is available [here](<https://www.hass-agent.io/latest/contributing/reporting-issues/#permalinks>)."

            if "setup | question" in tags:
                users_to_ping.add(638245963240046592)

            tags_embed.description += "\n\n**We will help as soon as possible.**\nWhile you're waiting you can try the following:\n> - Checkout [the documentation](<https://hass-agent.io/>).\n> - Search here in discord for previously solved similar issues."

            # Send Embeds
            await asyncio.sleep(5)
            try:
                await thread.send(
                    embed=mark_solution_embed,
                    file=nextcord.File("/app/bot/mark_solution.png"),
                )
                await thread.send(embed=tags_embed)

                # Mention users
                for user_id in users_to_ping:
                    user = self.bot.get_user(user_id)
                    if user:
                        await thread.send(user.mention)
            except nextcord.HTTPException as e:
                print(f"Failed to send message to thread: {e}")


def setup(bot):
    bot.add_cog(GetHelpCog(bot))
