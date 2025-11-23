import discord
from discord.ext import commands
import requests
import random
import string
import os

# ---------------- Settings ----------------
TOKEN = os.getenv("BOT_TOKEN")   # Discord bot token from Render Environment
BACKEND_URL = os.getenv("BACKEND_URL")  # Render backend URL
# ------------------------------------------

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Needed for DMs & member info

bot = commands.Bot(command_prefix="!", intents=intents)

# --------- Helper function ---------
def generate_key(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# --------- Commands ---------
@bot.command()
async def verify(ctx):
    user_id = str(ctx.author.id)
    key = generate_key()

    # Backend ko save karna
    resp = requests.post(f"{BACKEND_URL}/create_key", json={
        "user": user_id,
        "key": key
    })

    if resp.status_code == 200:
        await ctx.author.send(f"✅ Your key: `{key}`\nUse this key inside Roblox.")
        await ctx.reply("DM me check karo — key bhej di!")
    else:
        await ctx.reply("❌ Tumhare paas already ek key hai.")

@bot.command()
async def lock(ctx, key):
    await ctx.reply("⚙️ HWID lock Roblox script se auto hoga.")

# --------- Start Bot ---------
bot.run(TOKEN)
