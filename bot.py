import os
import random
from dotenv import load_dotenv
import discord
from discord import app_commands, Activity, ActivityType

# Charger le token depuis Render Environment Variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# === Configuration ===
ALLOWED_GUILD_ID = 1396857214546874378  # Remplace par ton serveur
ROLE_ID = 1443515266234581052           # Remplace par le rôle à ping

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Statut du bot
@client.event
async def on_ready():
    await tree.sync()
    activity = Activity(type=ActivityType.watching, name="vos commandes !")
    await client.change_presence(activity=activity)
    print(f"🤖 Connecté en tant que {client.user}")

# Limiter le bot aux serveurs autorisés
@client.event
async def on_guild_join(guild):
    if guild.id != ALLOWED_GUILD_ID:
        await guild.leave()
        print(f"🚫 J'ai quitté le serveur non autorisé : {guild.name}")

# === Commandes ===

# /ping
@tree.command(name="ping", description="Le bot répond Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong 🏓")

# /echo
@tree.command(name="echo", description="Répète ton message")
async def echo(interaction: discord.Interaction, texte: str):
    await interaction.response.send_message(texte)

# Liste de 100 questions du jour
questions = [
    "Quelle est ta couleur préférée ?",
    "Quel est ton plat préféré ?",
    "Quelle série regardes-tu en ce moment ?",
    "Quel est ton film préféré de tous les temps ?",
    "Si tu pouvais voyager n’importe où, où irais-tu ?",
    "Quel est ton animal préféré ?",
    "Quelle est ta chanson préférée ?",
    "Quel est ton super-héros préféré ?",
    "Plutôt café ou thé ?",
    "Plutôt chat ou chien ?",
    "Quel est ton jeu vidéo préféré ?",
    "Si tu avais un super-pouvoir, lequel choisirais-tu ?",
    "Quelle est ta saison préférée ?",
    "Quel est ton fruit préféré ?",
    "Quel est ton dessert préféré ?",
    "Quel est ton passe-temps favori ?",
    "Quelle est ta boisson préférée ?",
    "Quelle est ta destination de vacances de rêve ?",
    "Quel est ton personnage de fiction préféré ?",
    "Si tu pouvais rencontrer une célébrité, qui choisirais-tu ?",
    "Quel est ton sport préféré ?",
    "Plutôt plage ou montagne ?",
    "Si tu pouvais changer quelque chose dans le monde, quoi ?",
    "Quel est ton hobby créatif préféré ?",
    "Quelle langue aimerais-tu apprendre ?",
    "Plutôt lever tôt ou coucher tard ?",
    "Si tu pouvais vivre dans une autre époque, laquelle ?",
    "Quel est ton souvenir d’enfance préféré ?",
    "Plutôt sucré ou salé ?",
    "Si tu gagnais à la loterie, que ferais-tu en premier ?",
    "Quel est ton plat que tu cuisines le mieux ?",
    "Plutôt Netflix ou YouTube ?",
    "Quel est ton film d’animation préféré ?",
    "Quel est ton instrument de musique préféré ?",
    "Quel pays aimerais-tu visiter un jour ?",
    "Plutôt ville ou campagne ?",
    "Si tu pouvais maîtriser un instrument du jour au lendemain, lequel ?",
    "Quelle est ta couleur de vêtements préférée ?",
    "Quel est ton jeu de société préféré ?",
    "Plutôt sucré ou amer ?",
    "Quel est ton moyen de transport préféré ?",
    "Si tu pouvais rencontrer un personnage historique, qui choisirais-tu ?",
    "Quelle est ta matière scolaire préférée ?",
    "Plutôt lecture ou film ?",
    "Si tu devais vivre dans une série TV, laquelle ?",
    "Quel est ton emoji préféré ?",
    "Plutôt hiver ou été ?",
    "Quel est ton légume préféré ?",
    "Quel est ton pays préféré parmi ceux que tu as visités ?",
    "Plutôt téléphone ou ordinateur ?",
    "Quel est ton snack préféré ?",
    "Si tu pouvais parler à ton futur toi, que lui dirais-tu ?",
    "Quel est ton réseau social préféré ?",
    "Plutôt film d’horreur ou comédie ?",
    "Quel est ton manga ou anime préféré ?",
    "Si tu pouvais changer une chose chez toi, laquelle ?",
    "Quel est ton endroit préféré dans ta ville ?",
    "Plutôt sucré ou glacé ?",
    "Quel est ton film Disney préféré ?",
    "Quel est ton genre musical préféré ?",
    "Si tu pouvais vivre dans un jeu vidéo, lequel ?",
    "Plutôt neige ou pluie ?",
    "Quel est ton dessert français préféré ?",
    "Si tu pouvais rencontrer un personnage de jeu vidéo, lequel ?",
    "Quel est ton fruit exotique préféré ?",
    "Plutôt pizza ou burger ?",
    "Quel est ton parfum de glace préféré ?",
    "Si tu pouvais apprendre une compétence instantanément, laquelle ?",
    "Quel est ton animal sauvage préféré ?",
    "Plutôt montagne russe ou grande roue ?",
    "Quel est ton acteur ou actrice préféré(e) ?",
    "Si tu pouvais vivre dans un film, lequel ?",
    "Plutôt aventure ou détente ?",
    "Quel est ton film d’action préféré ?",
    "Si tu pouvais changer ta couleur de cheveux, laquelle choisirais-tu ?",
    "Quel est ton plat étranger préféré ?",
    "Plutôt chocolat noir ou au lait ?",
    "Quel est ton livre préféré ?",
    "Si tu pouvais vivre n’importe où dans le monde, où ?",
    "Quel est ton style de musique préféré pour danser ?",
    "Plutôt mer ou lac ?",
    "Si tu pouvais rencontrer un animal mythique, lequel ?",
    "Quel est ton personnage Disney préféré ?",
    "Plutôt journée tranquille ou soirée animée ?",
    "Si tu pouvais avoir un objet magique, lequel ?",
    "Quel est ton film comique préféré ?",
    "Plutôt lever du soleil ou coucher du soleil ?",
    "Quel est ton plat italien préféré ?",
    "Si tu pouvais apprendre une nouvelle langue instantanément, laquelle ?",
    "Plutôt pizza ou pâtes ?",
    "Quel est ton personnage de dessin animé préféré ?",
    "Si tu pouvais être un animal pour une journée, lequel serais-tu ?",
    "Quel est ton jeu préféré sur téléphone ?",
    "Plutôt montagnes ou plage pour les vacances ?",
    "Quel est ton endroit préféré pour te détendre ?",
    "Si tu pouvais rencontrer un dieu de la mythologie, lequel ?",
    "Quel est ton personnage de film préféré ?",
    "Plutôt sucré ou épicé ?",
    "Si tu pouvais inventer quelque chose, ce serait quoi ?",
    "Quel est ton sport extrême préféré ?",
    "Plutôt lire un livre ou écouter un podcast ?",
    "Si tu pouvais remonter le temps, à quelle époque irais-tu ?",
    "Quel est ton réseau social préféré ?",
    "Plutôt film ou série ?"
]

# /qdj
@tree.command(name="qdj", description="Envoie la question du jour")
async def qdj(interaction: discord.Interaction):
    if interaction.guild.id != ALLOWED_GUILD_ID:
        await interaction.response.send_message("❌ Ce bot n'est pas autorisé sur ce serveur.", ephemeral=True)
        return

    role = interaction.guild.get_role(ROLE_ID)
    qdj_text = random.choice(questions)

    embed = discord.Embed(
        title="❓ Question du Jour",
        description=qdj_text,
        color=discord.Color.blue()
    )
    embed.set_footer(text="Répondez dans le thread ci-dessous !")

    msg = await interaction.channel.send(content=role.mention, embed=embed)
    thread = await msg.create_thread(name="Réponses à la Question du Jour", auto_archive_duration=1440)
    await thread.send("Répondez ici ! 📝")

    await interaction.response.send_message("✅ Question du jour publiée !", ephemeral=True)

# Lancer le bot
client.run(TOKEN)
