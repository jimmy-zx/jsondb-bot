import os
import dotenv

import discord
from jsondb_bot import App


dotenv.load_dotenv()
token = os.getenv('DISCORD_TOKEN')
dbfile = os.getenv('DBFILE', 'regs.json')

try:
    with open(dbfile, 'r') as f:
        regs = json.load(f)
except FileNotFoundError:
    regs = {}

intents = discord.Intents.default()
intents.message_content = True
app = App(intents, regs=regs)

app.client.run(token)

with open(dbfile, 'w') as f:
    json.dump(app.regs, f)
