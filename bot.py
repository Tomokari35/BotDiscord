import os
from dotenv import load_dotenv
import discord
from discord import app_commands

# Charger le TOKEN depuis le fichier .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents (permissions du bot pour lire messages etc.)
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Commande /ping
@tree.command(name="ping", description="Le bot répond Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong 🏓")
@tree.command(name="hello", description="Le bot te dit bonjour")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Salut 👋, comment ça va ? 😄")
# Commande /echo
@tree.command(name="echo", description="Répète ton message")
async def echo(interaction: discord.Interaction, texte: str):
    await interaction.response.send_message(texte)
@tree.command(name="say", description="Le bot répète ton message")
async def say(interaction: discord.Interaction, texte: str):
    await interaction.response.send_message(f"Tu as dit : {texte}")


from discord import Activity, ActivityType

@client.event
async def on_ready():
    
    allowed_guilds = [1396857214546874378]  # ID du serveur autorisé

@client.event
async def on_guild_join(guild):
    if guild.id not in allowed_guilds:
        await guild.leave()
        
from discord import Activity, ActivityType
@client.event
async def on_ready():
    await tree.sync()
    # Statut “Regarde …”
    activity = Activity(type=ActivityType.watching, name="Sakura High FR RP")
    await client.change_presence(activity=activity)
    print(f"🤖 Connecté et regarde vos commandes")

client.run(TOKEN)



