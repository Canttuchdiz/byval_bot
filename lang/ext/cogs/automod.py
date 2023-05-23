from discord import Interaction, AutoModRuleEventType, AutoModRuleTriggerType, \
    AutoModRuleActionType, AutoModTrigger, AutoModRuleAction, HTTPException
from discord.app_commands import command, Group, autocomplete, Choice
from discord.ext.commands import Cog, Bot
import traceback


class AutoModCog(Cog):
    group = Group(name="rule", description="The group behind all automod commands.")

    def __int__(self, bot: Bot) -> None:
        self.client = bot

    async def trigger_autocomplete(self, interaction: Interaction, current: str) -> list:

        try:

            return [Choice(name=t_type.name, value=str(t_type.value)) for t_type in AutoModRuleTriggerType if
                    current.lower() in t_type.name.lower()]

        except Exception as e:
            traceback.print_exc()

    @group.command(name="create", description="Creates an automod rule.")
    @autocomplete(am_trigger=trigger_autocomplete)
    async def create_rule(self, interaction: Interaction, name: str, am_trigger: str, enabled: bool) -> None:
        try:
            trigger = AutoModRuleTriggerType(int(am_trigger))
            await interaction.guild.create_automod_rule(name=name,
                                                        event_type=AutoModRuleEventType.message_send,
                                                        trigger=AutoModTrigger(type=trigger),
                                                        actions=[AutoModRuleAction()], enabled=enabled)
            await interaction.response.send_message("Rule successfully added!")
        except HTTPException as e:
            await interaction.response.send_message("Rule already exists.")


async def setup(bot) -> None:
    await bot.add_cog(AutoModCog(bot))
