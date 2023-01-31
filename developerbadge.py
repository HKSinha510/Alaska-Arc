import discord
import inspect
from discord import app_commands, Intents, Client, Interaction
token=3
class Bot(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        """ This is called when the bot boots, to setup the global commands """
        await self.tree.sync()

client = Bot(intents=Intents.none())


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")


@client.tree.command()
async def hello(interaction: Interaction):
    """ Says hello or something """
    # Responds in the console that the command has been ran
    

    # Then responds in the channel with this message
    await interaction.response.send_message(inspect.cleandoc(f"""
        Hi **{interaction.user}**, thank you for saying hello to me.
        > __**Where's my badge?**__
        > Eligibility for the badge is checked by Discord in intervals,
        > at this moment in time, 24 hours is the recommended time to wait before trying.
        > __**It's been 24 hours, now how do I get the badge?**__
        > If it's already been 24 hours, you can head to
        > https://discord.com/developers/active-developer and fill out the 'form' there.
        > __**Active Developer Badge Updates**__
        > Updates regarding the Active Developer badge can be found in the
        > Discord Developers server -> https://discord.gg/discord-developers - in the #active-dev-badge channel.
    """))

# Runs the bot with the token you provided

client.run(token)
