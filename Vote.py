import discord
import topgg

bot = discord.Client()
# This example uses topggpy's webhook system.
bot.topgg_webhook = topgg.WebhookManager(bot).dbl_webhook("http://62.171.128.234", "password")

# The port must be a number between 1024 and 49151.
bot.topgg_webhook.run(2240)  # this method can be awaited as well


@bot.event
async def on_dbl_vote(data):
    """An event that is called whenever someone votes for the bot on Top.gg."""
    if data["type"] == "test":
        # this is roughly equivalent to
        # `return await on_dbl_test(data)` in this case
        return bot.dispatch("dbl_test", data)

    print(f"Received a vote:\n{data}")


@bot.event
async def on_dbl_test(data):
    """An event that is called whenever someone tests the webhook system for your bot on Top.gg."""
    print(f"Received a test vote:\n{data}")