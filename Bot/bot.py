import discord
import json
from discord.ext import commands

with open('config.json', 'r') as config_file:
    config = json.load(config_file)


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='-', intents=intents)


def has_specific_role(role_id):
    def predicate(ctx):
        role = discord.utils.get(ctx.guild.roles, id=role_id)
        if role is None:
            raise commands.CommandError(f"Le rôle avec l'ID {role_id} n'existe pas sur ce serveur.")
        
        return role in ctx.author.roles
    
    return commands.check(predicate)


def load_objects():
    with open('objects.json', 'r') as objects_file:
        return json.load(objects_file)


def save_objects(objects):
    with open('objects.json', 'w') as objects_file:
        json.dump(objects, objects_file, indent=4)


@bot.command(name='add')
@has_specific_role(123456789012345678)  # Remplacez 123456789012345678 par l'ID de votre rôle spécifique
async def add_object(ctx, name, quantity: int):
    name_lower = name.lower()  
    objects = load_objects()
    
    if name_lower in objects:
        objects[name_lower] += quantity
    else:
        objects[name_lower] = quantity
    
    save_objects(objects)
    await ctx.send(f'Objet ajouté : {name} ({quantity})')


@bot.command(name='stock')
@has_specific_role(123456789012345678) # Remplacez 123456789012345678 par l'ID de votre rôle spécifique
async def stock(ctx):
    objects = load_objects()
    if not objects:
        await ctx.send('Aucun objet n\'est disponible pour le moment.')
    else:
        embed = discord.Embed(title='Stock des objets Minecraft')
        for name, quantity in objects.items():
            embed.add_field(name=name, value=f'Quantité : {quantity}', inline=False)
        await ctx.send(embed=embed)


@bot.command(name='change')
@has_specific_role(123456789012345678)  # Remplacez 123456789012345678 par l'ID de votre rôle spécifique
async def change(ctx, name, quantity: int):
    try:
        name_lower = name.lower()  
        objects = load_objects()
        
        if name_lower in objects:
            objects[name_lower] = quantity
            save_objects(objects)
            await ctx.send(f'Quantité de l\'objet {name} modifiée à {quantity}')
        else:
            await ctx.send(f'L\'objet {name} n\'existe pas dans le stock.')
    except Exception as e:
        await ctx.send(f'Erreur lors du changement de quantité : {e}')


@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')

bot.run(config['token'])
