import requests
import discord
from discord.ext import commands
import api

TOKEN = "OTI5Njg5NTc3MTY4NDQxMzk0.Ydq-4w.t075-NSdKUxHp7_aIbB_8koHgjI"
client = commands.Bot(command_prefix='?')
PATH = "/home/csgoservers/serverfiles4/css/maps/"

@client.command(alias=["r", "rq", "dl"])
async def request(ctx, arg1):
    url = arg1
    mod_id = url.rsplit('/', 1)[-1]

    j = api.GamebananaAPI(mod_id).get_json()


    if j["_aGame"]["_sName"] == "Counter-Strike: Source":

        mapName = j["_sName"] or "Unknown"
        mapCreator = j["_aSubmitter"]["_sName"] or "Unknown"
        mapCreatorAvatarUrl = j["_aSubmitter"]["_sAvatarUrl"] or "https://images.gamebanana.com/static/img/defaults/avatar.gif"
        mapDownloadUrl = j["_aFiles"][0]["_sDownloadUrl"] or ""
        mapFile = j["_aFiles"][0]["_sFile"]
        mapUploadDate = api.get_date(j["_aFiles"][0]["_tsDateAdded"])

        print(f"{mapName} by {mapCreator}")
        print(mapUploadDate)
        print(mapDownloadUrl)

        api.download_file(mapDownloadUrl, mapName)

    else:
        await ctx.send("Game must be css")


@client.event
async def on_ready():
    print('Logged in as: {}'.format(client.user))


client.remove_command("help")
client.run(TOKEN)
