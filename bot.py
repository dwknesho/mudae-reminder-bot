import os
from datetime import datetime
from zoneinfo import ZoneInfo

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ROLE_ID = int(os.getenv("ROLE_ID"))

PH_TZ = ZoneInfo("Asia/Manila")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # needed so the bot can add/remove roles on members

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    allowed_mentions=discord.AllowedMentions(roles=True, everyone=False, users=True),
)

reminders_on = True
_last_fired_key = None  # (date, hour) — stops the message from firing twice in the same window


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    if not reset_check.is_running():
        reset_check.start()


@tasks.loop(seconds=30)
async def reset_check():
    """Checks every 30s so we don't miss :21 even if the loop drifts slightly."""
    global _last_fired_key

    if not reminders_on:
        return

    now = datetime.now(PH_TZ)
    is_awake_hours = now.hour >= 9 or now.hour < 2  # active 9:00 AM to 1:59 AM
    if now.minute == 21 and is_awake_hours:
        key = (now.date(), now.hour)
        if key != _last_fired_key:
            _last_fired_key = key
            channel = bot.get_channel(CHANNEL_ID)
            if channel is not None:
                await channel.send(f"<@&{ROLE_ID}> Mudae pulls have reset")
            else:
                print(f"Could not find channel with ID {CHANNEL_ID}. Check your .env file.")


@reset_check.before_loop
async def before_reset_check():
    await bot.wait_until_ready()


@bot.command()
async def subscribe(ctx):
    """Gives the caller the reminder role."""
    role = ctx.guild.get_role(ROLE_ID)
    if role is None:
        await ctx.send("Couldn't find that role. Check ROLE_ID in the bot's .env file.")
        return
    if role in ctx.author.roles:
        await ctx.send("You already have the reminder role.")
        return
    try:
        await ctx.author.add_roles(role, reason="Subscribed to Mudae reset reminders")
        await ctx.send(f"Gave you **{role.name}** — you'll get pinged every hour at :21 PH time.")
    except discord.Forbidden:
        await ctx.send(
            "I don't have permission to give that role."
            
        )


@bot.command()
async def unsubscribe(ctx):
    """Removes the reminder role from the caller."""
    role = ctx.guild.get_role(ROLE_ID)
    if role is None:
        await ctx.send("Couldn't find that role.")
        return
    if role not in ctx.author.roles:
        await ctx.send("You don't have the reminder role.")
        return
    try:
        await ctx.author.remove_roles(role, reason="Unsubscribed from Mudae reset reminders")
        await ctx.send(f"Removed **{role.name}** — you won't get pinged anymore.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to remove that role.")

@bot.command()
async def testreminder(ctx):
    """Manually fires the reminder message right now, for testing."""
    await ctx.send(f"<@&{ROLE_ID}> Mudae pulls have reset")
    
@bot.command()
async def remindon(ctx):
    global reminders_on
    reminders_on = True
    await ctx.send("Mudae reset reminders are **ON** for the server.")


@bot.command()
async def remindoff(ctx):
    global reminders_on
    reminders_on = False
    await ctx.send("Mudae reset reminders are **OFF** for the server.")


@bot.command()
async def remindstatus(ctx):
    now = datetime.now(PH_TZ)
    role = ctx.guild.get_role(ROLE_ID)
    role_name = role.name if role else "unknown role"
    await ctx.send(
        f"Reminders are currently {'ON' if reminders_on else 'OFF'} (pinging **{role_name}**).\n"
        f"Current PH time: {now.strftime('%I:%M %p')}\n"
        f"Use `!subscribe` / `!unsubscribe` to join or leave the reminder role."
    )


if __name__ == "__main__":
    if not DISCORD_TOKEN:
        raise SystemExit("DISCORD_TOKEN is missing. Did you create a .env file from .env.example?")
    bot.run(DISCORD_TOKEN)
