import discord
from discord.ext import commands
import requests
import random
import string
import os

# ---------------- Settings ----------------
TOKEN = os.getenv("BOT_TOKEN")   # Token env variable se aayega
BACKEND_URL = "https://key-system-backend.onrender.com"
# ------------------------------------------

intents = discord.Intents.default()
intents.message_content = True

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
        await ctx.reply("Key DM me bhej di hai!")
    else:
        await ctx.reply("❌ Tumhare paas already ek key hai.")

@bot.command()
async def lock(ctx, key):
    await ctx.reply("⚙️ HWID lock automatically Roblox script se hoga.")

# --------- Start Bot ---------
bot.run(TOKEN)
