import os
import random
from dotenv import load_dotenv
import discord
from discord import app_commands, Activity, ActivityType

# Charger le token depuis Render Environment Variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# === Configuration ===
ALLOWED_GUILD_ID = 1396857214546874378  # ID de ton serveur
ROLE_ID = 1443515266234581052           # ID du rôle à ping
ALLOWED_ROLES = [
    1396857328216707103,
    1396984978717409421,
    1396962683844300810,
    1405281099612950528,
    1416810690945093662,
    1428466417681825854,
    1410239639423553606
]
# === Salons de logs ===
LOGS_MESSAGES = 1441063853080444928      # ID salon pour messages
LOGS_MODERATION = 1443553704308510750   # ID salon pour modération
LOGS_COMMANDS = 1443553865692745739     # ID salon pour commandes

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# --- Fonctions utilitaires ---
def role_required():
    async def predicate(interaction: discord.Interaction) -> bool:
        return any(role.id in ALLOWED_ROLES for role in interaction.user.roles)
    return app_commands.check(predicate)

async def send_log(channel_id: int, title: str, description: str, color=discord.Color.green()):
    channel = client.get_channel(channel_id)
    if channel:
        embed = discord.Embed(title=title, description=description, color=color)
        await channel.send(embed=embed)

# === Statut du bot ===
@client.event
async def on_ready():
    await tree.sync()
    activity = Activity(type=ActivityType.watching, name="Sakura High FR RP | On vous aime <3")
    await client.change_presence(activity=activity)
    print(f"🤖 Connecté en tant que {client.user}")

# === Limiter le bot aux serveurs autorisés ===
@client.event
async def on_guild_join(guild):
    if guild.id != ALLOWED_GUILD_ID:
        await guild.leave()
        print(f"🚫 J'ai quitté le serveur non autorisé : {guild.name}")

# === Logs modération ===
@client.event
async def on_member_join(member):
    await send_log(LOGS_MODERATION, "Nouveau membre", f"{member.mention} a rejoint le serveur.")

@client.event
async def on_member_remove(member):
    await send_log(LOGS_MODERATION, "Membre parti", f"{member.mention} a quitté le serveur.")

@client.event
async def on_member_ban(guild, user):
    await send_log(LOGS_MODERATION, "Membre banni", f"{user.mention} a été banni.", color=discord.Color.dark_red())

@client.event
async def on_member_unban(guild, user):
    await send_log(LOGS_MODERATION, "Membre débanni", f"{user.mention} a été débanni.", color=discord.Color.dark_green())

# === Logs messages ===
@client.event
async def on_message_delete(message):
    if message.author.bot:
        return
    desc = f"Message de {message.author.mention} supprimé dans {message.channel.mention} :\n{message.content}"
    await send_log(LOGS_MESSAGES, "Message supprimé", desc, color=discord.Color.red())

# === Commandes ===

# /ping
@tree.command(name="ping", description="Le bot répond Pong!")
@role_required()
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong 🏓")
    await send_log(LOGS_COMMANDS, "Commande /ping", f"{interaction.user.mention} a utilisé la commande /ping", color=discord.Color.blue())

# /echo
@tree.command(name="echo", description="Répète ton message")
@role_required()
async def echo(interaction: discord.Interaction, texte: str):
    await interaction.response.send_message(texte)
    await send_log(LOGS_COMMANDS, "Commande /echo", f"{interaction.user.mention} a utilisé /echo : {texte}", color=discord.Color.blue())

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
@role_required()
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
    await send_log(LOGS_COMMANDS, "Commande /qdj", f"{interaction.user.mention} a publié la question : {qdj_text}", color=discord.Color.blue())


# Booster
BOOST_CHANNEL_ID = 1399499262647075057  # salon pour afficher les boosts
BOOST_GIF = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZTB6Z29iZDhrdGppaXRjcWZveDI0bHppanJ1ajdzcGY4Zmpwend2YiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Xl0oVz3eb9mfu/giphy.gif"  # GIF à afficher

@client.event
async def on_member_update(before, after):
    # Vérifie si la personne a commencé à booster le serveur
    if not before.premium_since and after.premium_since:
        channel = client.get_channel(BOOST_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                title=f"✨ Merci à toi {after.name} pour le boost !",
                description="Ton soutien fait vivre le serveur ! 💖",
                color=discord.Color.purple()
            )
            embed.set_thumbnail(url=after.display_avatar.url)
            embed.set_image(url=BOOST_GIF)
            await channel.send(embed=embed)

            # Envoi un MP au booster
            try:
                dm_embed = discord.Embed(
                    title="Merci pour ton boost ! ✨",
                    description="Ton soutien nous aide beaucoup, MERCIII !",
                    color=discord.Color.purple()
                )
                dm_embed.set_image(url=BOOST_GIF)
                await after.send(embed=dm_embed)
            except:
                print(f"Impossible d'envoyer un MP à {after.name}")
# ----- TEST -----
@tree.command(name="testboost", description="Teste l'embed de boost")
@role_required()
async def testboost(interaction: discord.Interaction):
    user = interaction.user  # on utilise la personne qui lance la commande
    channel = client.get_channel(BOOST_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title=f"✨ Merci à toi {user.name} pour le boost !",
            description="Ton soutien fait vivre le serveur ! 💖",
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_image(url=BOOST_GIF)
        await channel.send(embed=embed)

        # Envoi un MP de test
        try:
            dm_embed = discord.Embed(
                title="Merci pour ton boost ! ✨",
                description="Ton soutien nous aide beaucoup ! Profite des avantages du serveur !",
                color=discord.Color.purple()
            )
            dm_embed.set_image(url=BOOST_GIF)
            await user.send(embed=dm_embed)
        except:
            await interaction.response.send_message("Impossible d'envoyer le MP de test.", ephemeral=True)

    await interaction.response.send_message("✅ Test boost envoyé !", ephemeral=True)


# Bienvenue
WELCOME_GIF = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZTB6Z29iZDhrdGppaXRjcWZveDI0bHppanJ1ajdzcGY4Zmpwend2YiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/DIYVI7Iz4dmnu/giphy.gif"  # GIF de bienvenue

@client.event
async def on_member_join(member):
    # Log modération
    await send_log(LOGS_MODERATION, "Nouveau membre", f"{member.mention} a rejoint le serveur.")

    # Envoi MP de bienvenue
    try:
        embed = discord.Embed(
            title=f"Bienvenue {member.name} ! 🎉",
            description=(
                "Bienvenue sur **Sakura High FR RP** !\n\n"
                "Voici ce que tu peux faire sur le serveur :\n"
                "- Lire les règles\n"
                "- Participer aux salons\n"
                "- Découvrir les événements et QdJ\n"
            ),
            color=discord.Color.green()
        )
        embed.set_image(url=WELCOME_GIF)
        await member.send(embed=embed)
    except:
        print(f"Impossible d'envoyer un MP à {member.name}")
# ----- TEST -----
@tree.command(name="testarriver", description="Teste l'embed de bienvenue")
@role_required()
async def testarriver(interaction: discord.Interaction):
    user = interaction.user  # on utilise la personne qui lance la commande
    try:
        embed = discord.Embed(
            title=f"Bienvenue {user.name} ! 🎉",
            description=(
                "Bienvenue sur **Sakura High FR RP** !\n\n"
                "Voici ce que tu peux faire sur le serveur :\n"
                "- Lire les règles\n"
                "- Participer aux salons\n"
                "- Découvrir les événements et QDJ\n"
            ),
            color=discord.Color.green()
        )
        embed.set_image(url=WELCOME_GIF)
        await user.send(embed=embed)
    except:
        await interaction.response.send_message("Impossible d'envoyer le MP de test.", ephemeral=True)
        return

    await send_log(LOGS_MODERATION, "Test arrivée", f"{user.mention} a reçu l'embed de bienvenue (test).")
    await interaction.response.send_message("✅ Test arrivée envoyé !", ephemeral=True)





# Gestion des erreurs pour les checks de rôle
@tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message("❌ Vous n'avez pas la permission pour utiliser cette commande.", ephemeral=True)

# === Lancer le bot ===
client.run(TOKEN)


