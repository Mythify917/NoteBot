import discord
from discord.ext import commands
import json
from datetime import datetime
from keep_alive import keep_alive

def prefix(bot, message):
    if not message.guild:
        return ''
    else:
        return ['n!', "<@!787900820489895966> "]

bot = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=discord.Intents.all())
bot.remove_command('help')

@bot.event
async def on_ready():
    print("ok")
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"notes."))

@bot.command()
async def start_notes(ctx):
    with open('notes.json', 'r') as f:
        notes = json.load(f)
         
    print("json file loaded")
    
    if str(ctx.author.id) in notes.keys():
        await ctx.send("You are already in the database!")
        return
    
    else:
        notes[str(ctx.author.id)] = {}
        notes[str(ctx.author.id)]['notes'] = []
        notes[str(ctx.author.id)]['notes_formatted'] = []

        with open("notes.json", "w") as f:
            json.dump(notes, f, indent=4)
        
        await ctx.send("You are now in the database!")

@bot.command()
async def note(ctx, *, note):
    with open('notes.json', 'r') as f:
        notes = json.load(f)

    if str(ctx.author.id) not in notes.keys():
        await ctx.send("You aren't in the database! Use `n!start_notes` to be entered.")
        return

    notes[str(ctx.author.id)]['notes_formatted'].append(f"{len(notes[str(ctx.author.id)]['notes'])+1}. {note} - {datetime.strftime(ctx.message.created_at, '%b %d %Y, %-I:%M %p')} UTC")
    notes[str(ctx.author.id)]['notes'].append(note)
    

    with open('notes.json', 'w') as f:
        json.dump(notes, f, indent=4)
    

    await ctx.send(f"I have successfully taken note of `{note}`!")

@bot.command()
async def notes(ctx):
    with open('notes.json', 'r') as f:
        notes = json.load(f)

    if str(ctx.author.id) not in notes.keys():
        await ctx.send("You aren't in the database! Use `n!start_notes` to be entered.")
        return

    
    embed = discord.Embed(title="Your Notes", color=discord.Color.red(), timestamp=datetime.now())

    if str(notes[str(ctx.author.id)]['notes']) == '[]':
        notes_list = "None"
    
    else:
        notes_list = '\n'.join(notes[str(ctx.author.id)]['notes_formatted'])
    
    embed.description = notes_list
    embed.set_footer(text=f"{len(notes[str(ctx.author.id)]['notes'])} total notes!", icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)


@bot.command()
async def del_note(ctx, note):
    with open('notes.json', 'r') as f:
        notes = json.load(f)

    if str(ctx.author.id) not in notes.keys():
        await ctx.send("You aren't in the database! Use `n!start_notes` to be entered.")
        return
    
    if note.lower() == "all":
        await ctx.send("Are you sure you want to delete all your notes? (y/n)")
        def check(m):
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
        
        y_or_n = await bot.wait_for('message', check=check)
        if y_or_n.content.lower() in ["y", 'yes']:
            notes[str(ctx.author.id)]['notes'] = []
            notes[str(ctx.author.id)]['notes_formatted'] = []
            await ctx.send("Successfully deleted all notes!")
        elif y_or_n.content.lower() in ['n', 'no']:
            await ctx.send("I haven't deleted your notes!")
        
        else:
            await ctx.send("Not a valid option!")
    else:
        try:
            note_content = notes[str(ctx.author.id)]['notes'][int(note)-1]
            notes[str(ctx.author.id)]['notes'].pop(int(note)-1)
            notes[str(ctx.author.id)]['notes_formatted'].pop(int(note)-1)
            await ctx.send(f"Successfully deleted the note **{note_content}**!")
        except IndexError:
            await ctx.send("I couldn't find that note!")

    with open('notes.json', 'w') as f:
        json.dump(notes, f, indent=4)

        
@bot.command()
async def help(ctx):
    embed = discord.Embed(color=discord.Color.red(), title="NoteBot Help", timestamp=ctx.message.created_at)
    embed.description = open('help.txt').read()
    embed.set_footer(text=f" {ctx.author} | <> = Required Arguments", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"You are missing a required argument, {ctx.author.mention}!")
    
    raise error

keep_alive()
bot.run('Nzg3OTAwODIwNDg5ODk1OTY2.X9br0g.PqZ9fj7TbDWp2PncePOtRv4bJgg')