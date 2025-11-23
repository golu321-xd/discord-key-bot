import discord
from discord.ext import commands
import requests
import random
import string
import os
from flask import Flask
import threading

# ---------------- Settings ----------------
TOKEN = os.getenv("BOT_TOKEN")   # Secure method
BACKEND_URL = "https://key-system-backend.onrender.com"
# ------------------------------------------

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Important for privileged intents

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

# --------- Simple HTTP server for Render ---------
app = Flask("")

@app.route("/")
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# Flask server ko alag thread me start karo
threading.Thread(target=run_flask).start()

# --------- Start Bot ---------
bot.run(TOKEN)
