from discord.ext import commands
import discord
from Webscrape import Image, parser, infotable, clean, Conversion, webmachine, load
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

# Token is the .env token variable
TOKEN = os.environ.get("DISCORD_TOKEN")
# Command prefix is for whenever calling a command there is a prefix, it is usually "!", but it can be customized
COMMAND = os.environ.get("COMMAND_PREFIX")

Bot = commands.Bot(command_prefix=COMMAND)

# Store the value of load() into a variable called Lookup
Lookup = load()

# When the bot is ready:
@Bot.event
async def on_ready():
    # Print the bot's Token and command prefix
    print(f"Token: {TOKEN}\nCommand: {COMMAND}")

# Facts command takes three arguments, itself, Type of info, e.g obtain, table, etc, The objects's name.
@Bot.command(name='Fact', help='Usage: !Fact (Type of Info) (Name)')
async def Fact(ctx, arg1, *args):
    # Declare text
    text = ""
    # Creates the url
    url = f"https://minecraft.gamepedia.com/{'_'.join(args)}"
    # Stores the html contents into a variable
    General = Conversion(parser(url))
    # Creates a embed format
    embed = discord.Embed(title=f"General information of {' '.join(args).capitalize()}",
                          url=url)

    # Sets the image to the object image
    embed.set_image(url=str(Image(parser(url))))
    # Capitalize the Object's name
    Argument = arg1.capitalize()

    # If the info type is table, then add a field called Info and its value will the information table.
    if Argument == "Table":
        embed.add_field(name="Info",
                        value=infotable(url))

    # See if the info type is a actual info type
    elif arg1.capitalize() in Lookup:
        # Text will store the desired information
        text = clean(webmachine(Lookup[Argument], General))
        # Add the info to the embedded message
        embed.add_field(name=arg1.capitalize(),
                        value=str(text))

    # if not, well something went wrong
    else:
        # Text is a now a message telling the user that something happened
        text = f"Looks like something went wrong! Need help? try {COMMAND}help"
        embed.add_field(name="Error",
                        value=text)

    # Print the length of the text
    print(len(text))
    # If the length of text is longer than discord's character limit
    if len(text) >= 2000:
        # Add a field to tell them that the text is too big
        embed.add_field(name='Failed to send', value=f"Look The information That {ctx.author.mention} requested went over Discord's character limit, So here's the link: {url}")

        # Remove the information so the bot can actually send this info
        embed.remove_field(0)

        # Send
        await ctx.send(embed=embed)

    # So if the text length in not bigger than Discord's character limit, but bigger than Discord's embedded character limit.
    elif 2000 > len(text) > 1024:
        # Send the text in normal method
        await ctx.send(text)

    # If there is no issue
    else:
        # Just send the message
        await ctx.send(embed=embed)


# A command for a more in depth guide to use Fact command
@Bot.command(name="Helps", help=f"Provides a more in depth way of using {COMMAND}fact command")
async def explain(ctx):

    # Creates a embedded message
    embed = discord.Embed(title=f"A Guide To Using {COMMAND}Fact",
                          description=f"Usage: {COMMAND}Fact (Type of Info) (Name)")

    # More detail about info types
    embed.add_field(name="Info Types",
                    value="""
                    Table: Provides a table of general info.
                    Obtain: Provides info on how to get the object.
                    Trivia: Provides facts about the object.
                    Usage: Provide info on how to use the object.
                    Spawning: Provides info on where the mob spawns.
                    Drops: Provides info on the drops of the mob.
                    Behavior: Provides info on how the mob acts.""", inline=True)

    # How to use the command
    embed.add_field(name="Examples",
                    value=f"""
                    Usage: {COMMAND}Fact Table Dirt
                    Usage: {COMMAND}Fact Obtain Diamonds""", inline=True)

    # Errors the user might encounter
    embed.add_field(name="Errors",
                    value="""
                    You will encounter errors. these Errors happened because of multiple reasons:
                    1. The Object name provide does not exist.
                    2. Discord character limit, prevents the information being sent.
                    3. The specific information type for the object does not exist.
                    4. If a message was sent, but not in embedded form, That was because of Discord's embedded character limit.
                    5. If a error appears and does not match the above errors, contact the developer.""", inline=False)

    # Send embedded message
    await ctx.send(embed=embed)

# In case of a error relating to a command
@Bot.event
async def on_command_error(ctx, error):
    # If the error is command related
    if isinstance(error, commands.errors.CommandInvokeError):
        # print the error
        print(error)
        # Tell the user to get help
        await ctx.send(f"{ctx.author.mention}, You have used this command incorrectly, please refer to {COMMAND}help or {COMMAND}Helps for help.")


Bot.run(TOKEN)
