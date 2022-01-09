import requests
import discord
from discord.ext import commands

import api

TOKEN = "OTI5Njg5NTc3MTY4NDQxMzk0.Ydq-4w.FajL8Noot9I56xR_HXkaHU-lfOs"
client = commands.Bot(command_prefix='?')


j = api.GamebananaAPI(mod_id).get_json

@client.command(alias=["r", "rq", "dl"])
async def request(ctx, arg1):
    url = arg1
    mod_id = url.rsplit('/', 1)[-1]

    if  j["_aGame"]["_sName"] == "Counter-Strike: Source":    
        team_url = j["_AfiliatedStudio"]["_sProfileUrl"] 
        submitter = j["_aSubmitter"]["_sName"]

        download_url = j["_aFiles"]["_sDownloadUrl"]

    else:
        await ctx.send("Game must be css")

@client.event
async def on_ready():
    print('Logged in as: {}'.format(client.user))

client.remove_command("help")
client.run(TOKEN)
