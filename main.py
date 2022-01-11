import discord
from discord import Color
from discord.ext import commands
from hurry.filesize import size
import api
import yaml


with open("config.yml", "r") as file:
    cfg = yaml.safe_load(file)


TOKEN = cfg['token']
client = commands.Bot(command_prefix=cfg['prefix'])


@client.command(aliases=["r", "rq", "dl"])
async def request(ctx, arg1):
    url = arg1
    mod_id = url.rsplit('/', 1)[-1]

    j = api.GamebananaAPI(mod_id).get_json()

    if (cfg['game_check'] == 1 and j['_aGame']['_sAbbreviation'] in cfg['games']) or cfg['game_check'] == 0:

        name = j["_sName"] or "Unknown"
        creator = j["_aSubmitter"]["_sName"] or "Unknown"
        creator_avatar_url = j["_aSubmitter"][
                                 "_sAvatarUrl"] or "https://images.gamebanana.com/static/img/defaults/avatar.gif"
        map_image = j["_aPreviewMedia"][0]["_sFile"] or ""

        download_url = j["_aFiles"][0]["_sDownloadUrl"]
        map_file = j["_aFiles"][0]["_sFile"]
        upload_date = api.get_date(j["_aFiles"][0]["_tsDateAdded"])

        api.download_file(url=download_url, file=map_file, path=cfg['paths'][j['_aGame']['_sAbbreviation']], name)

        embed = discord.Embed(title=f"{name} by {creator}",
                              description=f"Upload Date: {upload_date} \n Download URL: {download_url} \n "
                                          f"Game: {j['_aGame']['_sAbbreviation']}",
                              colour=Color.blurple()
                              )
        embed.set_footer(text="Size: " + size(j["_aFiles"][0]["_nFilesize"]),
                         icon_url="https://cdn.discordapp.com/icons/"
                                  "639948169643425792/ac76d8508b89af4403b01dd7893a4b14.webp")
        embed.set_image(url=f'https://images.gamebanana.com/img/ss/mods/{map_image}')
        embed.set_thumbnail(url=creator_avatar_url)

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')

    else:
        await ctx.send(f"{j['_aGame']['_sAbbreviation']} is not listed under supported games in config.yml")


@client.event
async def on_ready():
    print(f'Logged in as: {client.user}')


client.remove_command("help")
client.run(TOKEN)
