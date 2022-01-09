import requests
import discord
from discord.ext import commands
from hurry.filesize import size
import api

TOKEN = "OTI5Njg5NTc3MTY4NDQxMzk0.Ydq-4w.t075-NSdKUxHp7_aIbB_8koHgjI"
client = commands.Bot(command_prefix='?')


@client.command(aliases=["r", "rq", "dl"])
async def request(ctx, arg1):
    url = arg1
    mod_id = url.rsplit('/', 1)[-1]

    j = api.GamebananaAPI(mod_id).get_json()

    if j["_aGame"]["_sAbbreviation"] == "CS:S":

        name = j["_sName"] or "Unknown"
        creator = j["_aSubmitter"]["_sName"] or "Unknown"
        creator_avatar_url = j["_aSubmitter"][
                                 "_sAvatarUrl"] or "https://images.gamebanana.com/static/img/defaults/avatar.gif"
        map_image = j["_aPreviewMedia"][0]["_sFile"] or ""

        download_url = j["_aFiles"][0]["_sDownloadUrl"]
        map_file = j["_aFiles"][0]["_sFile"]
        upload_date = api.get_date(j["_aFiles"][0]["_tsDateAdded"])

        api.download_file(download_url, name, map_file)

        embed = discord.Embed(title=f"{name} by {creator}",
                              description=f"Upload Date: {upload_date} \n Download URL: {download_url}"
                              )
        embed.set_footer(text="Size: " + size(j["_aFiles"][0]["_nFilesize"]), icon_url=creator_avatar_url)
        embed.set_image(url="https://images.gamebanana.com/img/ss/mods/" + map_image)
        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/639948169643425792/ac76d8508b89af4403b01dd7893a4b14.webp")

        await ctx.send(embed=embed)

    else:
        await ctx.send("Game must be css")


@client.event
async def on_ready():
    print('Logged in as: {}'.format(client.user))


client.remove_command("help")
client.run(TOKEN)
